"""Places Remember Django app config."""

from django.apps import AppConfig


class PlacesRememberConfig(AppConfig):
    """App configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "places_remember"
    verbose_name = "Places Remember"
