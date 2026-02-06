from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class UrlRecord(Base):
    """URL record model for storing shortened URLs."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    full_url = Column(String, nullable=False, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    created = Column(DateTime, default=datetime.utcnow)
