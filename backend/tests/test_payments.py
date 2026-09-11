from datetime import datetime, timezone

import pytest

from app.models import TransactionRecord
from app.services import mock_ledger, paystack_service


class FakeResponse:
    def __init__(self, data):
        self.data = data

    def raise_for_status(self):
        return None

    def json(self):
        return {"data": self.data}


class FakeClient:
    responses = []
    requests = []

    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def post(self, url, **kwargs):
        self.requests.append(("POST", url, kwargs))
        return FakeResponse(self.responses.pop(0))

    async def get(self, url, **kwargs):
        self.requests.append(("GET", url, kwargs))
        return FakeResponse(self.responses.pop(0))


@pytest.mark.asyncio
async def test_paystack_recipient_and_transfer_requests(monkeypatch):
    FakeClient.responses = [
        {"recipient_code": "RCP_test"},
        {"transfer_code": "TRF_test", "status": "pending"},
        {"transfer_code": "TRF_test", "status": "success"},
    ]
    FakeClient.requests = []
    monkeypatch.setattr(paystack_service.httpx, "AsyncClient", FakeClient)
    monkeypatch.setattr(paystack_service, "PAYSTACK_SECRET_KEY", "sk_test_key")

    recipient = await paystack_service.create_transfer_recipient("0123456789", "058", "Test Holder")
    transfer = await paystack_service.initiate_transfer(300000, recipient["recipient_code"], "Cash withdrawal")
    status = await paystack_service.get_transfer_status(transfer["transfer_code"])

    assert recipient["recipient_code"] == "RCP_test"
    assert transfer["transfer_code"] == "TRF_test"
    assert status["status"] == "success"
    assert FakeClient.requests[0][2]["json"] == {
        "type": "nuban",
        "name": "Test Holder",
        "account_number": "0123456789",
        "bank_code": "058",
        "currency": "NGN",
    }
    assert FakeClient.requests[1][2]["json"] == {
        "source": "balance",
        "amount": 300000,
        "recipient": "RCP_test",
        "reason": "Cash withdrawal",
    }


@pytest.mark.asyncio
async def test_mock_ledger_preserves_transfer_and_receipt_behavior():
    transfer = await mock_ledger.create_transfer(5000, "self")
    status = await mock_ledger.get_transaction_status(transfer["reference"])
    balance = await mock_ledger.get_account_balance("agent")
    tx = TransactionRecord(
        id="EP-2026-1",
        userId="user",
        action="withdraw",
        amount=5000,
        recipient=None,
        state="TRANSACTION_SUCCESS",
        createdAt=datetime.now(timezone.utc).isoformat(),
        paymentReference=transfer["reference"],
    )

    assert transfer["status"] == "success"
    assert status["status"] == "confirmed"
    assert balance["currency"] == "NGN"
    assert mock_ledger.generate_receipt(tx)["environment"] == "sandbox-mock"
