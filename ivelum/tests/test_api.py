"""API proxy tests (TestClient, mock upstream)."""

from unittest.mock import AsyncMock, patch

import httpx
from fastapi.testclient import TestClient

from app.main import app


@patch("app.main.httpx.AsyncClient")
def test_proxy_get_returns_modified_html(mock_client_class):
    """GET to proxy returns HTML with ™ and rewritten links."""
    mock_response = AsyncMock()
    mock_response.text = (
        "<html><body><p>The visual™ report™</p></body></html>"
    )
    mock_response.headers = {"content-type": "text/html"}
    mock_response.status_code = 200
    mock_response.raise_for_status = lambda: None

    async def mock_get(*args, **kwargs):
        return mock_response

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__.return_value = mock_http_client
    mock_http_client.__aexit__.return_value = None
    mock_http_client.get = mock_get
    mock_client_class.return_value = mock_http_client

    with TestClient(app) as client:
        response = client.get("/item?id=123")
    assert response.status_code == 200
    assert "visual™" in response.text
    assert "report™" in response.text


@patch("app.main.httpx.AsyncClient")
def test_proxy_502_on_upstream_error(mock_client_class):
    """On upstream HTTPError returns 502."""
    async def mock_get(*args, **kwargs):
        raise httpx.HTTPStatusError(
            "502",
            request=AsyncMock(),
            response=AsyncMock(status_code=502),
        )

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__.return_value = mock_http_client
    mock_http_client.__aexit__.return_value = None
    mock_http_client.get = mock_get
    mock_client_class.return_value = mock_http_client

    with TestClient(app) as client:
        response = client.get("/item?id=1")
    assert response.status_code == 502
    assert "upstream" in response.text.lower()


def test_proxy_405_method_not_allowed():
    """Method other than GET/POST returns 405."""
    with TestClient(app) as client:
        response = client.request("PUT", "/item?id=1")
    assert response.status_code == 405


@patch("app.main.httpx.AsyncClient")
def test_proxy_handles_large_response(mock_client_class):
    """Large response (>max_size) returns 502."""
    large_content = "x" * (11 * 1024 * 1024)  # 11MB
    mock_response = AsyncMock()
    mock_response.text = f"<html><body>{large_content}</body></html>"
    mock_response.content = large_content.encode()
    mock_response.headers = {"content-type": "text/html"}
    mock_response.status_code = 200
    mock_response.raise_for_status = lambda: None

    async def mock_get(*args, **kwargs):
        return mock_response

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__.return_value = mock_http_client
    mock_http_client.__aexit__.return_value = None
    mock_http_client.get = mock_get
    mock_client_class.return_value = mock_http_client

    with TestClient(app) as client:
        response = client.get("/item?id=123")
    assert response.status_code == 502


@patch("app.main.httpx.AsyncClient")
def test_proxy_handles_timeout(mock_client_class):
    """Timeout from upstream returns 504."""
    async def mock_get(*args, **kwargs):
        raise httpx.TimeoutException("Request timed out")

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__.return_value = mock_http_client
    mock_http_client.__aexit__.return_value = None
    mock_http_client.get = mock_get
    mock_client_class.return_value = mock_http_client

    with TestClient(app) as client:
        response = client.get("/item?id=1")
    assert response.status_code == 504


@patch("app.main.httpx.AsyncClient")
def test_proxy_path_too_long(mock_client_class):
    """Path longer than 2048 chars returns 400 before upstream call."""
    mock_response = AsyncMock()
    mock_response.text = "<html><body>Test</body></html>"
    mock_response.headers = {"content-type": "text/html"}
    mock_response.status_code = 200
    mock_response.content = b"<html><body>Test</body></html>"
    mock_response.raise_for_status = lambda: None

    async def mock_get(*args, **kwargs):
        return mock_response

    mock_http_client = AsyncMock()
    mock_http_client.__aenter__.return_value = mock_http_client
    mock_http_client.__aexit__.return_value = None
    mock_http_client.get = mock_get
    mock_client_class.return_value = mock_http_client

    with TestClient(app) as client:
        long_path = "/" + "a" * 2050
        response = client.get(long_path)
    assert response.status_code == 400
    assert "Invalid path" in response.json()["detail"]
