"""URL configuration for places_remember app."""

from django.urls import path

from . import views

app_name = "places_remember"

urlpatterns = [
    path("", views.index, name="index"),
    path("add-memory/", views.add_memory, name="add-memory"),
    path("logout/", views.logout_view, name="logout"),
    path("dev-login/", views.dev_login, name="dev-login"),
]
