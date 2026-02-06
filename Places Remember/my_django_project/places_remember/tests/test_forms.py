"""Tests for places_remember forms."""

import pytest
from places_remember.forms import MemoryForm


class TestMemoryForm:
    """Tests for MemoryForm."""

    def test_valid_data(self):
        """Form is valid with all required fields."""
        form = MemoryForm(
            data={
                "title": "Moscow",
                "comment": "Red Square",
                "lat": 55.7558,
                "lng": 37.6173,
            }
        )
        assert form.is_valid()
        assert form.cleaned_data["title"] == "Moscow"
        assert form.cleaned_data["lat"] == 55.7558

    def test_missing_lat_invalid(self):
        """Form is invalid when lat is missing."""
        form = MemoryForm(
            data={
                "title": "Place",
                "comment": "Comment",
                "lng": 37.6173,
            }
        )
        assert not form.is_valid()

    def test_missing_title_invalid(self):
        """Form is invalid when title is missing."""
        form = MemoryForm(
            data={
                "comment": "Comment",
                "lat": 55.0,
                "lng": 37.0,
            }
        )
        assert not form.is_valid()
