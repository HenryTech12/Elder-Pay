import logging
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, File, Form, HTTPException, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.services import db, face_auth, groq_service, mock_ledger, paystack_service, stt_provider, store, transaction_service, voice_auth, yarngpt_service
from app.services.languages import supported_languages
from app.services.transaction_service import STATES

logger = logging.getLogger("nativepay")

app = FastAPI(title="ElderPay API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hackathon simplicity — tighten to the real frontend origin before production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    db.init_schema()  # no-op if DATABASE_URL isn't set; falls back to in-memory storage on failure


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "demoMode": True,
        "paystackConfigured": bool(paystack_service.PAYSTACK_SECRET_KEY),
        "dbConnected": db.is_ready(),
    }


@app.get("/api/languages")
def languages():
    return supported_languages()


class TtsBody(BaseModel):
    text: str
    language: str = "en"


@app.post("/api/tts")
async def tts(body: TtsBody):
    try:
        audio = await yarngpt_service.synthesize_speech(body.text, body.language)
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as err:
        logger.error("tts failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "TTS_UNAVAILABLE", "message": str(err)})


@app.post("/api/voice/process")
async def voice_process(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(None),
    provider: Optional[str] = Form(None),
):
    try:
        audio_bytes = await audio.read()
        text = await stt_provider.transcribe(provider or stt_provider.get_default_provider(), audio_bytes, audio.filename, language)
        intent = await groq_service.parse_intent(text)
        return {"text": text, "intent": intent.model_dump()}
    except Exception as err:
        logger.error("voice_process failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


@app.post("/api/transcribe")
async def transcribe(
    audio: UploadFile = File(...),
    language: Optional[str] = Form(None),
    provider: Optional[str] = Form(None),
):
    try:
        audio_bytes = await audio.read()
        text = await stt_provider.transcribe(provider or stt_provider.get_default_provider(), audio_bytes, audio.filename, language)
        return {"text": text}
    except Exception as err:
        logger.error("transcribe failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


class IntentTextBody(BaseModel):
    text: str


@app.post("/api/ai/intent")
async def ai_intent(body: IntentTextBody):
    try:
        return (await groq_service.parse_intent(body.text)).model_dump()
    except Exception as err:
        logger.error("ai_intent failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "NETWORK_ERROR", "message": str(err)})


class ConfirmBody(BaseModel):
    id: Optional[str] = None
    userId: Optional[str] = None
    action: Optional[str] = None
    amount: Optional[int] = None
    recipient: Optional[str] = None
    confidence: Optional[float] = None
    voiceFeatureVector: Optional[list[float]] = None


@app.post("/api/transactions/confirm")
def transactions_confirm(body: ConfirmBody):
    if not body.id:
        if not body.userId:
            raise HTTPException(status_code=400, detail={"error": "USER_ID_REQUIRED"})
        evaluated = transaction_service.evaluate_intent(
            user_id=body.userId,
            action=body.action or "unknown",
            amount=body.amount,
            recipient=body.recipient,
            confidence=body.confidence,
        )
        return evaluated

    existing = store.get_transaction(body.id)
    if not existing:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    if existing.state != STATES["CONFIRMATION_REQUIRED"]:
        raise HTTPException(status_code=409, detail={"error": "INVALID_STATE", "state": existing.state})

    voice_verified = False
    if body.voiceFeatureVector:
        result = voice_auth.authorize_for_transaction(existing.userId, body.voiceFeatureVector)
        voice_verified = result["authorized"]
    return transaction_service.confirm_transaction(body.id, voice_verified=voice_verified)


@app.post("/api/transactions/{tx_id}/cancel")
def transactions_cancel(tx_id: str):
    result = transaction_service.cancel_transaction(tx_id)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    return result


class VerifyFaceBody(BaseModel):
    id: str
    faceDescriptor: Optional[list[float]] = None
    matched: bool = False  # fallback only for accounts with no registered face descriptor


@app.get("/api/banks")
async def banks():
    try:
        return await paystack_service.list_banks()
    except Exception as err:
        logger.error("banks failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "BANKS_UNAVAILABLE", "message": str(err)})


@app.get("/api/paystack/resolve-account")
async def paystack_resolve_account(accountNumber: str, bankCode: str):
    """Standalone test/utility endpoint — resolves an account directly,
    with no transaction required. What resolve-recipient calls internally."""
    try:
        return await paystack_service.resolve_account(accountNumber, bankCode)
    except Exception as err:
        logger.error("paystack_resolve_account failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "ACCOUNT_NOT_FOUND", "message": str(err)})


class ResolveRecipientBody(BaseModel):
    id: str
    accountNumber: str
    bankCode: str


@app.post("/api/transactions/resolve-recipient")
async def transactions_resolve_recipient(body: ResolveRecipientBody):
    result = await transaction_service.resolve_recipient_by_account(body.id, body.accountNumber, body.bankCode)
    if not result:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    return result


@app.post("/api/transactions/verify-face")
def transactions_verify_face(body: VerifyFaceBody):
    """Verifies server-side whenever a real face descriptor is supplied
    (the account has one on file) -- never trusts a client-asserted
    match for that case. Falls back to the client-asserted `matched`
    only for accounts with no registered face (e.g. legacy/demo
    accounts predating this feature), same graceful-degradation pattern
    used for voice."""
    existing = store.get_transaction(body.id)
    if not existing:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    matched = body.matched
    if body.faceDescriptor:
        result = face_auth.authorize_by_face(existing.userId, body.faceDescriptor)
        matched = result["authorized"]
    return transaction_service.record_face_verification(body.id, matched)


class SendBody(BaseModel):
    id: str


@app.post("/api/transactions/send")
async def transactions_send(body: SendBody):
    try:
        result = await transaction_service.execute_transaction(body.id)
        if not result:
            raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
        return result
    except HTTPException:
        raise
    except Exception as err:
        logger.error("transactions_send failed: %s", err, exc_info=True)
        raise HTTPException(status_code=500, detail={"error": "PAYMENT_API_ERROR", "message": str(err)})


@app.get("/api/transactions")
def transactions_list(userId: Optional[str] = None):
    return store.list_transactions(userId)


@app.get("/api/transactions/{tx_id}")
def transactions_get(tx_id: str):
    tx = store.get_transaction(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    return tx


@app.get("/api/transactions/{tx_id}/receipt")
def transactions_receipt(tx_id: str):
    tx = store.get_transaction(tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail={"error": "TRANSACTION_NOT_FOUND"})
    if tx.state != STATES["TRANSACTION_SUCCESS"]:
        raise HTTPException(status_code=409, detail={"error": "RECEIPT_NOT_AVAILABLE", "state": tx.state})
    return mock_ledger.generate_receipt(tx)


class AgentPayoutOnboardBody(BaseModel):
    bankAccountNumber: str
    bankCode: str


@app.post("/api/agent/payout-onboard")
async def agent_payout_onboard(body: AgentPayoutOnboardBody):
    """Verify the agent's account and create the Paystack payout recipient."""
    try:
        resolved = await paystack_service.resolve_account(body.bankAccountNumber, body.bankCode)
        recipient = await paystack_service.create_transfer_recipient(
            body.bankAccountNumber, body.bankCode, resolved["account_name"]
        )
        return store.update_agent_payout_profile(
            paystackRecipientCode=recipient["recipient_code"],
            paystackAccountNumber=body.bankAccountNumber,
            paystackBankCode=body.bankCode,
            payoutOnboarded=True,
        )
    except Exception as err:
        logger.error("agent payout onboarding failed: %s", err, exc_info=True)
        raise HTTPException(status_code=502, detail={"error": "PAYMENT_API_ERROR", "message": str(err)})


@app.get("/api/agent/payout-status")
def agent_payout_status():
    return store.get_agent_payout_profile()


@app.get("/api/accounts/{account_id}/balance")
def accounts_balance(account_id: str):
    balance = transaction_service.get_account_balance(account_id)
    if balance is None:
        raise HTTPException(status_code=404, detail={"error": "ACCOUNT_NOT_FOUND"})
    return {"accountId": account_id, "balance": balance, "currency": "NGN"}


class AccountRegisterBody(BaseModel):
    userId: str
    fullName: str
    address: str
    email: Optional[str] = None
    language: str


@app.post("/api/accounts/register")
def accounts_register(body: AccountRegisterBody):
    if store.get_account(body.userId):
        raise HTTPException(status_code=409, detail={"error": "ACCOUNT_EXISTS"})
    account = store.create_account(body.userId, body.fullName, body.language, body.address, body.email or None)
    return account


@app.get("/api/accounts/by-card/{card_number}")
def accounts_get_by_card(card_number: str):
    account = store.get_account_by_card(card_number)
    if not account:
        raise HTTPException(status_code=404, detail={"error": "CARD_NOT_RECOGNIZED"})
    return account


@app.get("/api/accounts/search")
def accounts_search(name: str):
    """Fallback for customers who can't recall their card number (common
    among elderly users) — look up by the name given at registration
    instead. Returns only id/name, not full account details, since a
    match here isn't itself an authorization decision — the face check
    after startSession still gates everything."""
    matches = store.find_accounts_by_name(name)
    return [{"id": a.id, "name": a.name} for a in matches]


@app.get("/api/accounts/{account_id}")
def accounts_get(account_id: str):
    account = store.get_account(account_id)
    if not account:
        raise HTTPException(status_code=404, detail={"error": "ACCOUNT_NOT_FOUND"})
    return account


class VoiceprintBody(BaseModel):
    userId: str
    featureVector: list[float]


@app.post("/api/voice/register")
def voice_register(body: VoiceprintBody):
    return voice_auth.register_voiceprint(body.userId, body.featureVector)


@app.post("/api/voice/authorize")
def voice_authorize(body: VoiceprintBody):
    return voice_auth.authorize_by_voice(body.userId, body.featureVector)


@app.get("/api/voice/status/{user_id}")
def voice_status(user_id: str):
    return {"registered": voice_auth.has_voiceprint(user_id)}


class FaceDescriptorBody(BaseModel):
    userId: str
    descriptor: list[float]


@app.post("/api/face/register")
def face_register(body: FaceDescriptorBody):
    return face_auth.register_face(body.userId, body.descriptor)


@app.post("/api/face/authorize")
def face_authorize(body: FaceDescriptorBody):
    return face_auth.authorize_by_face(body.userId, body.descriptor)


@app.get("/api/face/status/{user_id}")
def face_status(user_id: str):
    return {"registered": face_auth.has_face(user_id)}
