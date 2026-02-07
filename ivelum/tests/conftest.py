"""Pytest fixtures for API tests (TestClient)."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """HTTP client for app requests (no real upstream)."""
    return TestClient(app)
