"""
Pulls a small number of real, labeled code-switched clips from Intron's
AfriSwitch dataset (streaming — doesn't download the whole 6.84GB dataset)
and writes them into the benchmark manifest format.

AfriSwitch is a GATED dataset — you must have an approved access request
(check huggingface.co/settings/gated-repos or the dataset page for status)
AND be authenticated locally (`hf auth login` with a token from
huggingface.co/settings/tokens) before this will work. Running it before
approval will fail with a 401/403.

Confirmed schema (from the dataset card, 14 languages, "test" split only,
one config per language):
    audio                 — 16kHz HF Audio feature (bytes + path)
    language               — primary/matrix language of the utterance
    filename                — audio clip filename
    transcription            — verbatim human transcription (plain text)
    transcription_tagged  — same, with English spans wrapped in [[EN]]...[[/EN]]
    cmi                      — per-utterance code-mixing index
    num_switch_points     — per-utterance language-alternation count
    duration                — utterance length in seconds

Usage:
    pip install datasets soundfile --break-system-packages
    hf auth login   # once, with a token that has access to this gated dataset
    python fetch_afriswitch_clips.py

Adjust LANGUAGES / CLIPS_PER_LANGUAGE below to taste.
"""

import csv
import os

import soundfile as sf
from datasets import load_dataset

OUTPUT_AUDIO_DIR = "backend/benchmark/clips/afriswitch"
MANIFEST_PATH = "backend/benchmark/clips/manifest.csv"

# Config names are the full language names, per the dataset card
# (e.g. load_dataset("intronhealth/AfriSwitch", "hausa", split="test")).
# Nigerian-relevant configs for Includ:
LANGUAGES = ["yoruba", "hausa", "pidgin", "igbo"]
CLIPS_PER_LANGUAGE = 5

# language config name -> the code your app's languages.py / Sahara already use
LANG_CODE_MAP = {
    "yoruba": "yo",
    "hausa": "ha",
    "pidgin": "pcm",
    "igbo": "ig",
}

MANIFEST_HEADERS = [
    "audio_path", "reference_transcript", "language_pair", "domain",
    "accent_or_country", "device_type", "noise_condition", "expected_intent",
]


def main():
    os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
    manifest_exists = os.path.exists(MANIFEST_PATH)

    with open(MANIFEST_PATH, "a", newline="", encoding="utf-8") as manifest_file:
        writer = csv.writer(manifest_file)
        if not manifest_exists:
            writer.writerow(MANIFEST_HEADERS)

        for lang in LANGUAGES:
            print(f"Streaming {lang}...")
            # streaming=True: only fetches the shards it actually reads from,
            # not the full 6.84GB dataset. Only "test" split exists — this
            # is an eval-only benchmark release, not a training set.
            ds = load_dataset(
                "intronhealth/AfriSwitch", lang, split="test", streaming=True
            )

            lang_code = LANG_CODE_MAP.get(lang, lang)
            count = 0
            for example in ds:
                if count >= CLIPS_PER_LANGUAGE:
                    break

                audio = example.get("audio")
                transcript = example.get("transcription")

                if audio is None or not transcript:
                    continue

                filename = f"{lang}_{count:02d}.wav"
                out_path = os.path.join(OUTPUT_AUDIO_DIR, filename)
                sf.write(out_path, audio["array"], audio["sampling_rate"])

                writer.writerow([
                    out_path,
                    transcript,
                    f"{lang_code}-en",
                    "general",       # domain: real-world speech, not fintech-specific
                    "",              # accent_or_country: not provided (no annotator demographics released)
                    "",              # device_type
                    "",              # noise_condition: in-the-wild YouTube/podcast audio, unspecified
                    "",              # expected_intent: empty, this isn't banking-domain speech
                ])
                count += 1

            print(f"  saved {count} clips for {lang}")

    print(f"Done. Audio in {OUTPUT_AUDIO_DIR}/, rows appended to {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
