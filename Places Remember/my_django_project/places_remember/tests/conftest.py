"""Pytest configuration for places_remember tests."""

import pytest
from django.test import Client


@pytest.fixture
def client():
    """Django test client."""
    return Client()
