"""Run the three-provider code-switched STT benchmark.

Usage from the repository root:
    python -m backend.benchmark.run_benchmark

The runner never fabricates scores: unavailable audio and provider errors are
written as explicit failure rows and excluded from metric averages.
"""

import argparse
import asyncio
import csv
import logging
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# app/ is a top-level package when the backend is run from its own directory.
# Add that directory for the documented repository-root module invocation.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
load_dotenv(BACKEND_DIR / ".env")

from jiwer import cer, wer

from app.services import groq_service, stt_provider
from benchmark.dataset import BenchmarkClip, load_clips, resolve_audio_path

logger = logging.getLogger("stt-benchmark")
PROVIDERS = ("sahara", "groq", "local_whisper")
LANGUAGE_PAIRS = ("yo-en", "ha-en", "ig-en", "pcm-en", "en-en")


def normalize_transcript(text: str) -> str:
    """Lowercase, strip punctuation, and collapse whitespace for fair scoring."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def score_transcript(reference: str, actual: str) -> dict[str, float]:
    return {
        "wer_unnormalized": _metric(wer, reference, actual),
        "cer_unnormalized": _metric(cer, reference, actual),
        "wer_normalized": _metric(wer, normalize_transcript(reference), normalize_transcript(actual)),
        "cer_normalized": _metric(cer, normalize_transcript(reference), normalize_transcript(actual)),
    }


def _metric(metric, reference: str, actual: str) -> float:
    if not reference and not actual:
        return 0.0
    if not reference:
        return 1.0
    return float(metric(reference, actual))


async def run_clip(clip: BenchmarkClip, manifest_path: str, seen_sahara: bool) -> tuple[list[dict[str, Any]], bool]:
    path = resolve_audio_path(manifest_path, clip.audio_path)
    rows: list[dict[str, Any]] = []
    if not Path(path).is_file():
        error = f"audio file not found: {path}"
        for provider in PROVIDERS:
            rows.append(_failure_row(clip, provider, error))
        return rows, seen_sahara

    audio_bytes = Path(path).read_bytes()
    language_hint = clip.language_pair.split("-", 1)[0]
    for provider in PROVIDERS:
        if provider == "sahara":
            if seen_sahara:
                await asyncio.sleep(2.5)
            seen_sahara = True
        try:
            actual = await stt_provider.transcribe(
                provider,
                audio_bytes,
                Path(path).name,
                language_hint,
                use_domain_prompt=False,
            )
            row = {
                "audio_path": clip.audio_path,
                "language_pair": clip.language_pair,
                "domain": clip.domain,
                "provider": provider,
                "status": "ok",
                "error": "",
                "reference_transcript": clip.reference_transcript,
                "actual_transcript": actual,
                **score_transcript(clip.reference_transcript, actual),
            }
            if clip.expected_intent is not None:
                row.update(await _intent_scores(actual, clip.expected_intent))
            else:
                row.update(_empty_intent_scores())
        except Exception as error:  # one broken provider must not stop the benchmark
            logger.exception("%s failed for %s", provider, clip.audio_path)
            row = _failure_row(clip, provider, str(error))
        rows.append(row)
    return rows, seen_sahara


async def _intent_scores(actual: str, expected: dict[str, Any]) -> dict[str, Any]:
    try:
        parsed = await groq_service.parse_intent(actual)
        return {
            "intent_action_exact": int(_intent_value_equal(parsed.action, expected.get("action"), "action")),
            "intent_amount_exact": int(_intent_value_equal(parsed.amount, expected.get("amount"), "amount")),
            "intent_recipient_exact": int(_intent_value_equal(parsed.recipient, expected.get("recipient"), "recipient")),
        }
    except Exception as error:
        logger.exception("intent parsing failed")
        return {"intent_action_exact": 0, "intent_amount_exact": 0, "intent_recipient_exact": 0, "intent_error": str(error)}


def _intent_value_equal(actual: Any, expected: Any, field: str) -> bool:
    if actual is None or expected is None:
        return actual is expected
    if field == "amount":
        try:
            return Decimal(str(actual).strip()) == Decimal(str(expected).strip())
        except (InvalidOperation, ValueError):
            return False
    return str(actual).strip().casefold() == str(expected).strip().casefold()


def _empty_intent_scores() -> dict[str, Any]:
    return {"intent_action_exact": "", "intent_amount_exact": "", "intent_recipient_exact": "", "intent_error": ""}


def _failure_row(clip: BenchmarkClip, provider: str, error: str) -> dict[str, Any]:
    return {
        "audio_path": clip.audio_path,
        "language_pair": clip.language_pair,
        "domain": clip.domain,
        "provider": provider,
        "status": "failure",
        "error": error,
        "reference_transcript": clip.reference_transcript,
        "actual_transcript": "",
        "wer_unnormalized": "",
        "cer_unnormalized": "",
        "wer_normalized": "",
        "cer_normalized": "",
        **_empty_intent_scores(),
    }


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    fields = [
        "audio_path", "language_pair", "domain", "provider", "status", "error",
        "reference_transcript", "actual_transcript", "wer_unnormalized", "cer_unnormalized",
        "wer_normalized", "cer_normalized", "intent_action_exact", "intent_amount_exact",
        "intent_recipient_exact", "intent_error",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_report(rows: list[dict[str, Any]], output_path: Path) -> None:
    languages = sorted({row["language_pair"] for row in rows} or set(LANGUAGE_PAIRS))
    lines = ["# STT Benchmark Report", "", "Provider comparison on the clips listed in `clips/manifest.csv`.", "", "## Macro-average WER / CER", "", _table_header(languages, "WER / CER")]
    for language in languages:
        cells = [language]
        for provider in PROVIDERS:
            values = [row for row in rows if row["language_pair"] == language and row["provider"] == provider and row["status"] == "ok"]
            if not values:
                cells.append("n/a")
            else:
                cells.append(f"{_average(values, 'wer_normalized'):.3f} / {_average(values, 'cer_normalized'):.3f}")
        lines.append(_table_row(cells))

    fintech_intent_clips = {
        row["audio_path"]
        for row in rows
        if row["domain"] == "fintech" and row["intent_action_exact"] != ""
    }
    lines += [
        "",
        "## Intent exact-match accuracy",
        "",
        f"Intent scores are evaluated on a small set of {len(fintech_intent_clips)} real fintech utterances with expected intents.",
        "",
        _table_header(languages, "Action / Amount / Recipient"),
    ]
    for language in languages:
        cells = [language]
        for provider in PROVIDERS:
            values = [row for row in rows if row["language_pair"] == language and row["provider"] == provider and row["intent_action_exact"] != ""]
            if not values:
                cells.append("n/a")
            else:
                cells.append(" / ".join(f"{_average(values, field) * 100:.1f}%" for field in ("intent_action_exact", "intent_amount_exact", "intent_recipient_exact")))
        lines.append(_table_row(cells))

    lines += ["", "## Observed failure modes", ""]
    failures = [row for row in rows if row["status"] == "failure"]
    bad_transcripts = [row for row in rows if row["status"] == "ok" and float(row["wer_normalized"]) >= 0.75]
    if not failures and not bad_transcripts:
        lines.append("No provider failures or high-divergence clips observed.")
    else:
        for provider in PROVIDERS:
            provider_rows = [row for row in failures + bad_transcripts if row["provider"] == provider]
            if provider_rows:
                lines += [f"### {provider}", ""]
                for row in provider_rows:
                    actual = row["actual_transcript"] or (f"[failure] {row['error']}" if row["error"] else "[empty transcript]")
                    lines += [f"- `{row['audio_path']}`", f"  - Reference: {row['reference_transcript'] or '[not supplied]'}", f"  - Actual: {actual}"]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _average(rows: list[dict[str, Any]], field: str) -> float:
    return sum(float(row[field]) for row in rows) / len(rows)


def _table_header(languages: list[str], label: str) -> str:
    return _table_row(["Language pair", *PROVIDERS])


def _table_row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


async def main(manifest_path: str, results_dir: str) -> None:
    clips = load_clips(manifest_path)
    rows: list[dict[str, Any]] = []
    seen_sahara = False
    for clip in clips:
        clip_rows, seen_sahara = await run_clip(clip, manifest_path, seen_sahara)
        rows.extend(clip_rows)

    output_dir = Path(results_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, output_dir / "results.csv")
    write_report(rows, output_dir / "report.md")
    logger.info("Wrote %d provider rows to %s", len(rows), output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    default_root = Path(__file__).resolve().parent
    parser.add_argument("--manifest", default=str(default_root / "clips" / "manifest.csv"))
    parser.add_argument("--results-dir", default=str(default_root / "results"))
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    asyncio.run(main(args.manifest, args.results_dir))
