from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class UrlRecord(Base):
    """URL record model for storing shortened URLs."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True) 
    full_url = Column(String(2048), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    created = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
