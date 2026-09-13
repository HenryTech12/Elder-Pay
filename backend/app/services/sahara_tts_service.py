"""Sahara (Intron Voice API) text-to-speech integration."""

import asyncio
import os

import httpx

SAHARA_BASE_URL = os.environ.get("SAHARA_BASE_URL", "https://infer.voice.intron.io")
SAHARA_API_KEY = os.environ.get("SAHARA_API_KEY")

ACCENT_BY_LANGUAGE = {
    "en": "yoruba",
    "pcm": "pidgin",
    "yo": "yoruba",
    "ha": "hausa",
    "ig": "igbo",
}

SUPPORTED_LANGUAGES = {"en", "ha", "ig", "yo", "pcm"}
DEFAULT_GENDER = "female"


async def _poll_tts_status(client: httpx.AsyncClient, text_id: str, headers: dict) -> str:
    """Poll a queued Sahara TTS request until its audio URL is ready."""
    for _ in range(30):
        await asyncio.sleep(2)
        res = await client.get(
            f"{SAHARA_BASE_URL}/tts/v1/status/{text_id}",
            headers=headers,
        )
        res.raise_for_status()
        body = res.json()
        status = body.get("data", {}).get("processing_status")
        if status == "TTS_TEXT_AUDIO_GENERATED":
            return body["data"]["audio_path"]
        if status == "TTS_TEXT_PROCESSING_FAILED":
            raise RuntimeError(f"Sahara TTS failed for text_id={text_id}")
    raise TimeoutError(f"Sahara TTS still processing after polling, text_id={text_id}")


async def synthesize_speech(text: str, language: str) -> bytes:
    """Synthesize text and return WAV audio bytes."""
    if not SAHARA_API_KEY:
        raise RuntimeError("SAHARA_API_KEY not configured")

    headers = {"Authorization": f"Bearer {SAHARA_API_KEY}"}
    payload = {
        "text": text,
        "voice_language": language if language in SUPPORTED_LANGUAGES else "en",
        "voice_accent": ACCENT_BY_LANGUAGE.get(language, "yoruba"),
        "voice_gender": DEFAULT_GENDER,
        "output_audio_format": "wav",
    }

    async with httpx.AsyncClient(timeout=90.0) as client:
        res = await client.post(
            f"{SAHARA_BASE_URL}/tts/v1/generate",
            headers=headers,
            json=payload,
        )

        if res.status_code == 503:
            body = res.json()
            text_id = body.get("data", {}).get("text_id")
            if not text_id:
                res.raise_for_status()
            audio_path = await _poll_tts_status(client, text_id, headers)
        else:
            res.raise_for_status()
            body = res.json()
            audio_path = body.get("data", {}).get("audio_path")
            if not audio_path:
                raise RuntimeError(f"Sahara TTS response missing audio_path: {body}")

        audio_url = audio_path if audio_path.startswith("http") else f"{SAHARA_BASE_URL}{audio_path}"
        audio_res = await client.get(audio_url)
        audio_res.raise_for_status()
        return audio_res.content