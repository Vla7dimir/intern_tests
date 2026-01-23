from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


class UrlRecord(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    full_url = Column(String, nullable=False, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    created = Column(DateTime, default=datetime.utcnow)
