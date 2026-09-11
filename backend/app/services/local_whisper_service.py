"""Local open-source Whisper baseline backed by faster-whisper."""

import asyncio
import os
import tempfile
from pathlib import Path
from typing import Optional

_model = None

# medium is a reasonable accuracy/speed compromise for the benchmark; larger
# models can improve recognition but need substantially more memory and time.
_MODEL_SIZE = os.environ.get("LOCAL_WHISPER_MODEL_SIZE", "medium")
_WHISPER_LANGUAGES = {"en"}


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel

        _model = WhisperModel(_MODEL_SIZE)
    return _model


def _transcribe_file(path: str, language: Optional[str]) -> str:
    segments, _ = _get_model().transcribe(path, language=language)
    return " ".join(segment.text.strip() for segment in segments).strip()


async def transcribe_audio(
    audio_bytes: bytes,
    filename: str,
    language_hint: Optional[str] = None,
) -> str:
    suffix = Path(filename or "audio.webm").suffix or ".webm"
    language = language_hint if language_hint in _WHISPER_LANGUAGES else None
    with tempfile.NamedTemporaryFile(suffix=suffix) as audio_file:
        audio_file.write(audio_bytes)
        audio_file.flush()
        return await asyncio.to_thread(_transcribe_file, audio_file.name, language)