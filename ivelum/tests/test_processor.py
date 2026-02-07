"""HTML processing tests: ™, links, forms."""

from app.proxy.processor import process_html


def test_process_html_adds_trademark():
    """Words of exactly 6 letters get ™."""
    html = '<html><body><p>The visual report</p></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'visual™' in result
    assert 'report™' in result


def test_process_html_modifies_links():
    html = '<html><body><a href="/item?id=123">Link</a></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'href="http://127.0.0.1:8232/item?id=123"' in result


def test_process_html_modifies_full_urls():
    html = '<html><body><a href="https://news.ycombinator.com/item?id=123">Link</a></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'href="http://127.0.0.1:8232/item?id=123"' in result


def test_process_html_does_not_rewrite_fake_hn_domain():
    """Ссылки на поддельный хост (news.ycombinator.com.evil.com) не переписываются."""
    html = '<html><body><a href="https://news.ycombinator.com.evil.com/item">Link</a></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'https://news.ycombinator.com.evil.com/item' in result


def test_process_html_modifies_forms():
    html = '<html><body><form action="/submit"></form></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'action="http://127.0.0.1:8232/submit"' in result


def test_process_html_ignores_script_style():
    html = '<html><body><script>var visual = "test";</script></body></html>'
    result = process_html(html, 'http://127.0.0.1:8232')
    assert 'visual™' not in result


def test_process_html_empty_string_unchanged():
    """Empty or whitespace-only HTML is returned unchanged."""
    assert process_html("", "http://127.0.0.1:8232") == ""
    assert process_html("   ", "http://127.0.0.1:8232") == "   "


def test_process_html_form_full_url_with_trailing_slash_base():
    """Form with full HN URL is rewritten regardless of base format."""
    html = '<html><body><form action="https://news.ycombinator.com/submit">X</form></body></html>'
    result = process_html(html, "http://127.0.0.1:8232")
    assert 'action="http://127.0.0.1:8232/submit"' in result


def test_process_html_handles_invalid_proxy_url():
    """Invalid proxy_url returns original HTML."""
    html = '<html><body><p>Test</p></body></html>'
    result = process_html(html, "")
    assert "Test" in result


def test_process_html_handles_none_proxy_url():
    """None proxy_url returns original HTML."""
    html = '<html><body><p>Test</p></body></html>'
    result = process_html(html, None)  # type: ignore
    assert "Test" in result
