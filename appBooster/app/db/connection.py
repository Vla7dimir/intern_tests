"""Database connection and session management module."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from config.settings import settings

CONNECT_ARGS = {}
if settings.database_url.startswith("sqlite"):
    CONNECT_ARGS = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=CONNECT_ARGS,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True, 
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get database session.

    Yields:
        Database session.

    Note:
        Session is automatically closed in finally block.
        Any uncommitted transactions are rolled back on exception.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
