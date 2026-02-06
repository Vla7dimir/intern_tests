import secrets
import string
from typing import Optional

import httpx
from sqlalchemy.orm import Session
from urllib.parse import urlparse

from app.config import settings
from app.logger import get_logger
from app.models import UrlRecord

logger = get_logger(__name__)


def make_code(
    db: Session,
    size: Optional[int] = None,
    max_attempts: int = 100,
) -> str:
    """Generate unique random alphanumeric code.

    Args:
        db: Database session to check uniqueness.
        size: Optional code length. Uses default from settings if not provided.
        max_attempts: Maximum attempts to generate unique code.

    Returns:
        Unique random alphanumeric string.

    Raises:
        RuntimeError: If unable to generate unique code after max_attempts.
    """
    if size is None:
        size = settings.code_length
    alphabet = string.ascii_letters + string.digits

    logger.debug(
        "Generating unique code",
        extra={"size": size, "max_attempts": max_attempts},
    )
    for attempt in range(max_attempts):
        code = "".join(secrets.choice(alphabet) for _ in range(size))
        existing = db.query(UrlRecord).filter(UrlRecord.code == code).first()
        if not existing:
            logger.debug(
                "Unique code generated",
                extra={"code": code, "attempts": attempt + 1},
            )
            return code

    logger.error(
        "Failed to generate unique code",
        extra={"size": size, "max_attempts": max_attempts},
    )
    raise RuntimeError(
        f"Unable to generate unique code after {max_attempts} attempts"
    )


def check_url(url: str) -> bool:
    """Validate URL format and accessibility.

    Args:
        url: URL string to validate.

    Returns:
        True if URL is valid and accessible, False otherwise.
    """
    logger.debug("Validating URL", extra={"url": url})
    try:
        parts = urlparse(url)
        if not parts.scheme or not parts.netloc:
            logger.debug("URL validation failed: missing scheme or netloc")
            return False
        if parts.scheme not in ("http", "https"):
            logger.debug("URL validation failed: invalid scheme", extra={"scheme": parts.scheme})
            return False
        with httpx.Client(timeout=5.0, follow_redirects=True) as client:
            try:
                resp = client.head(url)
                is_valid = resp.status_code < 400
                logger.debug(
                    "URL validation result",
                    extra={"url": url, "status_code": resp.status_code, "is_valid": is_valid},
                )
                return is_valid
            except Exception as e:
                logger.debug("HEAD request failed, trying GET", extra={"url": url, "error": str(e)})
                resp = client.get(url)
                is_valid = resp.status_code < 400
                logger.debug(
                    "URL validation result (GET)",
                    extra={"url": url, "status_code": resp.status_code, "is_valid": is_valid},
                )
                return is_valid
    except Exception as e:
        logger.warning("URL validation failed with exception", extra={"url": url, "error": str(e)})
        return False


def check_code(code: str) -> bool:
    """Validate short code format.

    Args:
        code: Code string to validate.

    Returns:
        True if code is valid (3-50 alphanumeric, hyphens, underscores),
        False otherwise.
    """
    if not code or len(code) < 3 or len(code) > 50:
        return False
    allowed = string.ascii_letters + string.digits + "-_"
    return all(c in allowed for c in code)
