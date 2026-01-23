import secrets
import string
from urllib.parse import urlparse

import httpx

from app.config import settings


def make_code(size: int = None) -> str:
    if size is None:
        size = settings.code_length
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(size))


def check_url(url: str) -> bool:
    try:
        parts = urlparse(url)
        if not parts.scheme or not parts.netloc:
            return False
        if parts.scheme not in ("http", "https"):
            return False
        with httpx.Client(timeout=5.0, follow_redirects=True) as client:
            try:
                resp = client.head(url)
                return resp.status_code < 400
            except:
                resp = client.get(url)
                return resp.status_code < 400
    except:
        return False


def check_code(code: str) -> bool:
    if not code or len(code) < 3 or len(code) > 50:
        return False
    allowed = string.ascii_letters + string.digits + "-_"
    return all(c in allowed for c in code)
