"""Pytest fixtures for API tests."""

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from app.main import app  # noqa: E402
from app.db.connection import Base, engine, get_db  # noqa: E402
from app.models.experiment import Experiment, ExperimentOption  # noqa: E402

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def _seed_test_experiments(session: Session) -> None:
    """Insert initial experiments and options for tests.

    Args:
        session: Database session.
    """
    for key, options in [
        ("button_color", [("#FF0000", 33), ("#00FF00", 33), ("#0000FF", 34)]),
        ("price", [("10", 75), ("20", 10), ("50", 5), ("5", 10)]),
    ]:
        if session.query(Experiment).filter(Experiment.key == key).first():
            continue
        exp = Experiment(key=key)
        session.add(exp)
        session.commit()
        session.refresh(exp)
        for value, weight in options:
            session.add(
                ExperimentOption(experiment_key=key, value=value, weight=weight)
            )
        session.commit()


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """Database session with created tables and initial experiments.

    Yields:
        Database session for testing.
    """
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    _seed_test_experiments(db_session)
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db: Session) -> Generator[TestClient, None, None]:
    """HTTP client with test database session override.

    Args:
        db: Database session fixture.

    Yields:
        TestClient instance.
    """
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
