"""Tests for places_remember views."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from places_remember.models import Memory

User = get_user_model()


@pytest.mark.django_db
class TestIndexView:
    """Tests for index view."""

    def test_index_anonymous_returns_welcome_page(self, client):
        """Anonymous user gets welcome page with status 200."""
        response = client.get(reverse("places_remember:index"))
        assert response.status_code == 200
        assert b"Places Remember" in response.content
        assert b"Войти" in response.content or b"Google" in response.content

    def test_index_authenticated_returns_memory_list(self, client):
        """Authenticated user gets memory list page."""
        user = User.objects.create_user(username="testuser")
        client.force_login(user)
        response = client.get(reverse("places_remember:index"))
        assert response.status_code == 200
        assert b"Добавить воспоминание" in response.content or b"воспоминание" in response.content

    def test_index_authenticated_sees_own_memories(self, client):
        """Authenticated user sees only their memories."""
        user = User.objects.create_user(username="u")
        Memory.objects.create(user=user, title="My place", comment="x", lat=0, lng=0)
        client.force_login(user)
        response = client.get(reverse("places_remember:index"))
        assert response.status_code == 200
        assert b"My place" in response.content


@pytest.mark.django_db
class TestAddMemoryView:
    """Tests for add_memory view."""

    def test_add_memory_anonymous_redirects_to_index(self, client):
        """Anonymous user is redirected to index."""
        response = client.get(reverse("places_remember:add-memory"))
        assert response.status_code == 302
        assert response.url == reverse("places_remember:index")

    def test_add_memory_authenticated_get_shows_form(self, client):
        """Authenticated user gets the add-memory form."""
        user = User.objects.create_user(username="u")
        client.force_login(user)
        response = client.get(reverse("places_remember:add-memory"))
        assert response.status_code == 200
        assert b"Название" in response.content or b"Комментарий" in response.content
        assert b"map" in response.content

    def test_add_memory_post_creates_memory_and_redirects(self, client):
        """Valid POST creates memory and redirects to index."""
        user = User.objects.create_user(username="u")
        client.force_login(user)
        get_resp = client.get(reverse("places_remember:add-memory"))
        csrf_token = get_resp.context.get("csrf_token")
        if callable(csrf_token):
            csrf_token = csrf_token()
        else:
            csrf_token = str(csrf_token) if csrf_token else ""
        response = client.post(
            reverse("places_remember:add-memory"),
            {
                "title": "Paris",
                "comment": "Great trip",
                "lat": "48.8566",
                "lng": "2.3522",
                "csrfmiddlewaretoken": csrf_token,
            },
            follow=False,
        )
        assert response.status_code == 302
        assert response.url == reverse("places_remember:index")
        assert Memory.objects.filter(user=user, title="Paris").count() == 1


@pytest.mark.django_db
class TestLogoutView:
    """Tests for logout view."""

    def test_logout_redirects_to_index(self, client):
        """Logout redirects to index."""
        user = User.objects.create_user(username="u")
        client.force_login(user)
        response = client.get(reverse("places_remember:logout"))
        assert response.status_code == 302
        assert response.url == reverse("places_remember:index")
        response_next = client.get(reverse("places_remember:index"))
        assert b"Войти" in response_next.content or b"Google" in response_next.content
