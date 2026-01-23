import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.repository import find_by_code, save_url

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_repository.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


def test_save_url(db):
    record = save_url(db, "https://www.example.com")
    assert record.full_url == "https://www.example.com"
    assert record.code is not None
    assert len(record.code) == 6


def test_save_url_with_custom_code(db):
    record = save_url(db, "https://www.example.com", "custom-code")
    assert record.code == "custom-code"


def test_find_by_code(db):
    record = save_url(db, "https://www.example.com", "test-code")
    found = find_by_code(db, "test-code")
    assert found is not None
    assert found.code == "test-code"
    assert found.full_url == "https://www.example.com"


def test_find_by_code_not_found(db):
    found = find_by_code(db, "nonexistent")
    assert found is None
