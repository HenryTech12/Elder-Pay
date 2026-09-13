#!/usr/bin/env python3
"""
Live test of Sahara TTS against the real API.
Tests short phrase and long transaction confirmation (the one that broke YarnGPT).
"""

import asyncio
import time
import os
from dotenv import load_dotenv

load_dotenv()

from app.services.sahara_tts_service import synthesize_speech

SAHARA_API_KEY = os.environ.get("SAHARA_API_KEY")

if not SAHARA_API_KEY:
    print("ERROR: SAHARA_API_KEY not configured. Please set it in .env")
    exit(1)


async def test_tts(text: str, language: str, label: str):
    """Test TTS synthesis and measure response time."""
    print(f"\n[{label}]")
    print(f"  Language: {language}")
    print(f"  Text: {text[:80]}{'...' if len(text) > 80 else ''}")
    print(f"  Text length: {len(text)} chars")

    start_time = time.time()
    try:
        audio_bytes = await synthesize_speech(text, language)
        elapsed = time.time() - start_time

        print(f"  ✓ Success! Response time: {elapsed:.2f}s")
        print(f"  Audio size: {len(audio_bytes)} bytes")

        # Verify it's valid WAV (starts with RIFF header)
        if audio_bytes[:4] == b"RIFF":
            print(f"  ✓ Valid WAV format detected")
            return True
        else:
            print(f"  ✗ WARNING: Audio doesn't start with RIFF header. First 4 bytes: {audio_bytes[:4]}")
            return False

    except Exception as err:
        elapsed = time.time() - start_time
        print(f"  ✗ Failed after {elapsed:.2f}s: {err}")
        return False


async def main():
    print("=" * 70)
    print("SAHARA TTS LIVE TEST")
    print("=" * 70)

    results = []

    # Test 1: Short phrase in English
    results.append(
        await test_tts(
            "Hello, how are you today?",
            "en",
            "Short phrase (English)",
        )
    )

    # Test 2: Long phrase — the transaction confirmation that broke YarnGPT
    # This is a realistic e-commerce/fintech confirmation read-back
    long_text = "Your transfer of Fifty-Five Thousand Naira to Chioma Okafor at Zenith Bank, account ending in Four-Seven-One-Two, was confirmed at two forty-five PM on Thursday. A service fee of Seventy-Five Naira was charged. Your new balance is Two Hundred Twelve Thousand Naira."
    results.append(
        await test_tts(
            long_text,
            "en",
            "Long phrase (English) — transaction confirmation",
        )
    )

    # Test 3: Short phrase in Yoruba
    results.append(
        await test_tts(
            "Pẹlẹ o, e se wa",
            "yo",
            "Short phrase (Yoruba)",
        )
    )

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
