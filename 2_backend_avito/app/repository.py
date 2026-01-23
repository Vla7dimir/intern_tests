from sqlalchemy.orm import Session

from app.models import UrlRecord
from app.utils import make_code


def save_url(db: Session, url: str, code: str = None) -> UrlRecord:
    if not code:
        code = make_code()
        while db.query(UrlRecord).filter(UrlRecord.code == code).first():
            code = make_code()

    record = UrlRecord(full_url=url, code=code)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def find_by_code(db: Session, code: str) -> UrlRecord | None:
    return db.query(UrlRecord).filter(UrlRecord.code == code).first()
