from app.services.transcript_quality import is_likely_hallucinated


def test_repetitive_transcript_is_flagged():
    assert is_likely_hallucinated("send send send send money money money money", "en")


def test_clean_expected_language_transcript_is_not_flagged():
    assert not is_likely_hallucinated("Wo iye tó kù nínú àkáùntì mi", "yo")


def test_wrong_script_for_expected_language_is_flagged():
    assert is_likely_hallucinated("我亦都可以评论我的资料", "yo")
