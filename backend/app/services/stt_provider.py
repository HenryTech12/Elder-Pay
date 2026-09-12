"""Provider-agnostic speech-to-text dispatch."""

import os
from enum import Enum
from typing import Optional

from app.services import groq_service, local_whisper_service, sahara_service
from app.services.transcript_quality import is_likely_hallucinated


class STTProvider(str, Enum):
    GROQ = "groq"
    SAHARA = "sahara"
    LOCAL_WHISPER = "local_whisper"


DEFAULT_STT_PROVIDER = os.environ.get("DEFAULT_STT_PROVIDER", STTProvider.SAHARA.value)


def get_default_provider() -> str:
    return os.environ.get("DEFAULT_STT_PROVIDER") or DEFAULT_STT_PROVIDER


async def transcribe(
    provider: str,
    audio_bytes: bytes,
    filename: str,
    language_hint: Optional[str] = None,
    use_domain_prompt: bool = True,
) -> str:
    selected = provider or get_default_provider()
    try:
        selected_provider = STTProvider(selected)
    except ValueError as err:
        supported = ", ".join(item.value for item in STTProvider)
        raise ValueError(f"Unknown STT provider '{selected}'. Expected one of: {supported}") from err

    if selected_provider is STTProvider.GROQ:
        return await groq_service.transcribe_audio(
            audio_bytes, filename, language_hint, use_domain_prompt=use_domain_prompt
        )
    if selected_provider is STTProvider.SAHARA:
        return await sahara_service.transcribe_audio(audio_bytes, filename, language_hint)
    return await local_whisper_service.transcribe_audio(audio_bytes, filename, language_hint)


async def transcribe_with_quality(
    provider: str,
    audio_bytes: bytes,
    filename: str,
    language_hint: Optional[str] = None,
    use_domain_prompt: bool = True,
) -> tuple[str, bool]:
    transcript = await transcribe(
        provider,
        audio_bytes,
        filename,
        language_hint,
        use_domain_prompt=use_domain_prompt,
    )
    return transcript, not transcript.strip() or is_likely_hallucinated(transcript, language_hint)