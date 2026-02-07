"""Tests for add_trademark utility (™ after 6-letter words)."""

from app.utils.text import add_trademark


def test_add_trademark_empty_string():
    """Empty string is returned unchanged."""
    assert add_trademark("") == ""


def test_add_trademark_six_letter_words():
    """Words of exactly 6 letters get ™."""
    text = 'The visual report of the colliding files'
    result = add_trademark(text)
    assert 'visual™' in result
    assert 'report™' in result


def test_add_trademark_not_six_letters():
    """Words not exactly 6 letters are not modified."""
    text = 'The cat sat on mat'
    result = add_trademark(text)
    assert 'cat™' not in result
    assert 'sat™' not in result
    assert 'mat™' not in result


def test_add_trademark_mixed():
    """Mixed text: only 6-letter words get ™."""
    text = 'Basically, each PDF contains a single source'
    result = add_trademark(text)
    assert 'single™' in result
    assert 'source™' in result


def test_add_trademark_preserves_punctuation():
    """Punctuation and spaces are preserved."""
    text = 'Hello, world!'
    result = add_trademark(text)
    assert ',' in result
    assert '!' in result


def test_add_trademark_handles_none():
    """None input returns empty string."""
    result = add_trademark(None)  
    assert result == ""


def test_add_trademark_handles_non_string():
    """Non-string input is converted to string."""
    result = add_trademark(12345) 
    assert isinstance(result, str)
