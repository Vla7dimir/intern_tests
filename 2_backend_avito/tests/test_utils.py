import pytest

from app.utils import check_code, check_url, make_code


def test_make_code():
    code = make_code()
    assert len(code) == 6
    assert code.isalnum()


def test_make_code_custom_length():
    code = make_code(10)
    assert len(code) == 10


def test_check_url_valid():
    assert check_url("https://www.example.com") is True


def test_check_url_invalid_format():
    assert check_url("not-a-url") is False
    assert check_url("http://") is False
    assert check_url("ftp://example.com") is False


def test_check_code_valid():
    assert check_code("abc123") is True
    assert check_code("test-link") is True
    assert check_code("test_link") is True
    assert check_code("a" * 10) is True


def test_check_code_invalid():
    assert check_code("") is False
    assert check_code("ab") is False
    assert check_code("a" * 51) is False
    assert check_code("test@link") is False
    assert check_code("test link") is False
