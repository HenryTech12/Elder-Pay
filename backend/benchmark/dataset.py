"""CSV manifest loader for code-switched STT benchmark clips.

Manifest schema:
- audio_path: local audio file path, relative to the manifest directory or absolute.
- reference_transcript, language_pair, domain: required benchmark metadata.
- accent_or_country, device_type, noise_condition: optional recording metadata.
- expected_intent: optional JSON object with action, amount, and recipient keys.

Lines beginning with ``#`` and blank rows are ignored, so placeholder manifests
can document work still needed without being mistaken for recordings.
"""

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass(frozen=True)
class BenchmarkClip:
    audio_path: str
    reference_transcript: str
    language_pair: str
    domain: str
    accent_or_country: Optional[str] = None
    device_type: Optional[str] = None
    noise_condition: Optional[str] = None
    expected_intent: Optional[dict[str, Any]] = None


def load_clips(manifest_path: str) -> list[BenchmarkClip]:
    manifest = Path(manifest_path)
    clips: list[BenchmarkClip] = []
    with manifest.open("r", encoding="utf-8", newline="") as handle:
        rows = (line for line in handle if line.strip() and not line.lstrip().startswith("#"))
        for row in csv.DictReader(rows):
            expected_raw = (row.get("expected_intent") or "").strip()
            expected_intent = json.loads(expected_raw) if expected_raw else None
            clips.append(
                BenchmarkClip(
                    audio_path=_required(row, "audio_path"),
                    reference_transcript=row.get("reference_transcript", "").strip(),
                    language_pair=_required(row, "language_pair"),
                    domain=_required(row, "domain"),
                    accent_or_country=_optional(row.get("accent_or_country")),
                    device_type=_optional(row.get("device_type")),
                    noise_condition=_optional(row.get("noise_condition")),
                    expected_intent=expected_intent,
                )
            )
    return clips


def resolve_audio_path(manifest_path: str, audio_path: str) -> str:
    path = Path(audio_path)
    if path.is_absolute():
        return str(path)
    return str((Path(manifest_path).parent / path).resolve())


def _required(row: dict[str, str], key: str) -> str:
    value = (row.get(key) or "").strip()
    if not value:
        raise ValueError(f"Manifest column '{key}' is required")
    return value


def _optional(value: Optional[str]) -> Optional[str]:
    value = (value or "").strip()
    return value or None
