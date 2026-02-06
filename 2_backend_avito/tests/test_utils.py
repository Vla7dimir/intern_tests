import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base
from app.utils import check_code, check_url, make_code

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_utils.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    """Create test database session."""
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


def test_make_code(db: Session):
    """Test generating random code with default length."""
    code = make_code(db)
    assert len(code) == 6
    assert code.isalnum()


def test_make_code_custom_length(db: Session):
    """Test generating random code with custom length."""
    code = make_code(db, size=10)
    assert len(code) == 10


def test_check_url_valid():
    """Test checking valid URL."""
    assert check_url("https://www.example.com") is True


def test_check_url_invalid_format():
    """Test checking invalid URL formats."""
    assert check_url("not-a-url") is False
    assert check_url("http://") is False
    assert check_url("ftp://example.com") is False


def test_check_code_valid():
    """Test checking valid codes."""
    assert check_code("abc123") is True
    assert check_code("test-link") is True
    assert check_code("test_link") is True
    assert check_code("a" * 10) is True


def test_check_code_invalid():
    """Test checking invalid codes."""
    assert check_code("") is False
    assert check_code("ab") is False
    assert check_code("a" * 51) is False
    assert check_code("test@link") is False
    assert check_code("test link") is False
