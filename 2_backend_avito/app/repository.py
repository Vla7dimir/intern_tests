from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import CodeAlreadyExistsError, CodeNotFoundError
from app.logger import get_logger
from app.models import UrlRecord
from app.utils import make_code

logger = get_logger(__name__)


def save_url(db: Session, url: str, code: Optional[str] = None) -> UrlRecord:
    """Save URL with optional custom code.

    Args:
        db: Database session.
        url: Full URL to shorten.
        code: Optional custom code. If not provided, generates random code.

    Returns:
        Created UrlRecord instance.

    Raises:
        CodeAlreadyExistsError: If code already exists in database.
    """
    if code:
        logger.debug("Checking if custom code exists", extra={"code": code})
        existing = find_by_code(db, code)
        if existing:
            logger.warning("Custom code already exists", extra={"code": code})
            raise CodeAlreadyExistsError(f"Code '{code}' already exists")
    else:
        logger.debug("Generating random code")
        code = make_code(db)
        logger.debug("Random code generated", extra={"code": code})

    record = UrlRecord(full_url=url, code=code)
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
        logger.info(
            "URL saved successfully",
            extra={
                "code": code,
                "url_length": len(url),
            },
        )
        return record
    except IntegrityError as e:
        db.rollback()
        logger.error(
            "Integrity error while saving URL",
            extra={"code": code, "error": str(e)},
            exc_info=True,
        )
        # Проверяем, что это действительно дубликат кода
        if "code" in str(e.orig).lower() or "unique" in str(e.orig).lower():
            raise CodeAlreadyExistsError(f"Code '{code}' already exists") from e
        raise
    except Exception as e:
        db.rollback()
        logger.error(
            "Error while saving URL",
            extra={"code": code, "error": str(e)},
            exc_info=True,
        )
        raise


def find_by_code(db: Session, code: str) -> Optional[UrlRecord]:
    """Find URL record by code.

    Args:
        db: Database session.
        code: Short code to search for.

    Returns:
        UrlRecord if found, None otherwise.
    """
    return db.query(UrlRecord).filter(UrlRecord.code == code).first()


def get_by_code(db: Session, code: str) -> UrlRecord:
    """Get URL record by code or raise exception.

    Args:
        db: Database session.
        code: Short code to search for.

    Returns:
        UrlRecord instance.

    Raises:
        CodeNotFoundError: If code not found in database.
    """
    logger.debug("Looking up code in database", extra={"code": code})
    record = find_by_code(db, code)
    if not record:
        logger.warning("Code not found in database", extra={"code": code})
        raise CodeNotFoundError(f"Code '{code}' not found")
    logger.debug("Code found in database", extra={"code": code})
    return record
