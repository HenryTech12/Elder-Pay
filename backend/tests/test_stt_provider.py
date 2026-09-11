from unittest.mock import AsyncMock

import pytest

from app.services import groq_service, local_whisper_service, sahara_service, stt_provider


@pytest.mark.asyncio
async def test_unknown_provider_raises_clear_error():
    with pytest.raises(ValueError, match="Unknown STT provider 'unknown_provider'"):
        await stt_provider.transcribe("unknown_provider", b"audio", "clip.wav")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("provider", "service", "function_name"),
    [
        ("sahara", sahara_service, "transcribe_audio"),
        ("groq", groq_service, "transcribe_audio"),
        ("local_whisper", local_whisper_service, "transcribe_audio"),
    ],
)
async def test_dispatches_to_selected_provider(monkeypatch, provider, service, function_name):
    mocked = AsyncMock(return_value="transcript")
    monkeypatch.setattr(service, function_name, mocked)

    result = await stt_provider.transcribe(provider, b"audio", "clip.wav", "yo")

    assert result == "transcript"
    mocked.assert_awaited_once_with(b"audio", "clip.wav", "yo")
