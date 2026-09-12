"""Cheap safety heuristics for detecting likely hallucinated STT output."""

import re
import unicodedata
from collections import Counter
from typing import Optional


# These are intentionally small, high-signal words from the supported language
# prompts and known fintech clips. This is a safety net, not language detection;
# it can have false positives and false negatives.
_LANGUAGE_WORDS = {
    "yo": {"mo", "fe", "owo", "ranse", "akanti", "iye", "ku", "ninu", "mi", "si", "ni", "wo", "naira"},
    "ha": {"ina", "so", "in", "cire", "kudi", "tura", "asusun", "duba", "balance", "wace", "bank", "naira"},
    "ig": {"achoro", "m", "iziga", "ego", "nye", "akantuntu", "kedu", "nomba", "biko", "naira"},
}

_CJK_RANGES = ((0x3040, 0x30FF), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xAC00, 0xD7AF))
_CYRILLIC_RANGES = ((0x0400, 0x052F),)
_WORD_RE = re.compile(r"[\wÀ-ÖØ-öø-ÿ'’]+", re.UNICODE)


def _words(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKD", text.casefold())
    without_marks = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    return [word.replace("’", "'") for word in _WORD_RE.findall(without_marks)]


def _has_repeated_phrase(words: list[str]) -> bool:
    for phrase_length in range(2, len(words) // 3 + 1):
        phrases = [tuple(words[index:index + phrase_length]) for index in range(len(words) - phrase_length + 1)]
        counts = Counter(phrases)
        if any(count >= 3 for count in counts.values()):
            return True
    return False


def _is_in_ranges(codepoint: int, ranges: tuple[tuple[int, int], ...]) -> bool:
    return any(start <= codepoint <= end for start, end in ranges)


def _has_unrelated_script(text: str) -> bool:
    relevant = [char for char in text if not char.isspace() and not char.isdigit() and not unicodedata.category(char).startswith("P")]
    if not relevant:
        return False
    unrelated = sum(
        _is_in_ranges(ord(char), _CJK_RANGES) or _is_in_ranges(ord(char), _CYRILLIC_RANGES)
        for char in relevant
    )
    return unrelated / len(relevant) >= 0.3


def is_likely_hallucinated(text: str, expected_language: Optional[str] = None) -> bool:
    """Return whether non-empty STT output should be treated as unclear.

    Repetition catches Whisper-style loops. Script and vocabulary checks catch
    obvious wrong-language output. These cheap heuristics are not language
    detection and intentionally allow some false positives and false negatives.
    """
    words = _words(text)
    if _has_repeated_phrase(words):
        return True

    if expected_language not in _LANGUAGE_WORDS or len(words) <= 3:
        return _has_unrelated_script(text) if expected_language in _LANGUAGE_WORDS else False

    if _has_unrelated_script(text):
        return True

    vocabulary = _LANGUAGE_WORDS[expected_language]
    if not any(word in vocabulary for word in words):
        return True
    return False
