"""URL configuration for Places Remember project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("places_remember.urls")),
    path("", include("social_django.urls", namespace="social")),
]
