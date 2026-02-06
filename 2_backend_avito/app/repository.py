from typing import Optional

from sqlalchemy.orm import Session

from app.models import UrlRecord
from app.utils import make_code


def save_url(db: Session, url: str, code: Optional[str] = None) -> UrlRecord:
    """Save URL with optional custom code.

    Args:
        db: Database session.
        url: Full URL to shorten.
        code: Optional custom code. If not provided, generates random code.

    Returns:
        Created UrlRecord instance.
    """
    if not code:
        code = make_code()
        while db.query(UrlRecord).filter(UrlRecord.code == code).first():
            code = make_code()

    record = UrlRecord(full_url=url, code=code)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def find_by_code(db: Session, code: str) -> Optional[UrlRecord]:
    """Find URL record by code.

    Args:
        db: Database session.
        code: Short code to search for.

    Returns:
        UrlRecord if found, None otherwise.
    """
    return db.query(UrlRecord).filter(UrlRecord.code == code).first()
