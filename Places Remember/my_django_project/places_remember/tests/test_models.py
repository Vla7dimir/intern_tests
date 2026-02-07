"""Tests for places_remember models."""

import pytest
from django.contrib.auth import get_user_model

from places_remember.models import Memory

User = get_user_model()


@pytest.mark.django_db
class TestCustomUser:
    """Tests for CustomUser model."""

    def test_str_returns_username_when_no_name(self):
        """__str__ returns username when full name is empty."""
        user = User.objects.create_user(username="testuser")
        assert str(user) == "testuser"

    def test_str_returns_full_name_when_set(self):
        """__str__ returns full name when set."""
        user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
        )
        assert str(user) == "Test User"

    def test_avatar_url_optional(self):
        """avatar_url can be blank."""
        user = User.objects.create_user(username="u", avatar_url="")
        assert user.avatar_url == ""


@pytest.mark.django_db
class TestMemory:
    """Tests for Memory model."""

    def test_str_returns_title(self):
        """__str__ returns title."""
        user = User.objects.create_user(username="u")
        memory = Memory.objects.create(
            user=user,
            title="Paris",
            comment="Nice trip",
            lat=48.8566,
            lng=2.3522,
        )
        assert str(memory) == "Paris"

    def test_memory_belongs_to_user(self):
        """Memory is linked to user via FK."""
        user = User.objects.create_user(username="u")
        memory = Memory.objects.create(
            user=user,
            title="Place",
            comment="Comment",
            lat=0.0,
            lng=0.0,
        )
        assert memory.user == user
        assert list(user.memories.all()) == [memory]

    def test_ordering_by_created_at_desc(self):
        """Memories are ordered by created_at descending."""
        user = User.objects.create_user(username="u")
        m1 = Memory.objects.create(user=user, title="First", comment="c", lat=0, lng=0)
        m2 = Memory.objects.create(user=user, title="Second", comment="c", lat=0, lng=0)
        assert list(Memory.objects.filter(user=user)) == [m2, m1]
