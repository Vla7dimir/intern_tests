"""Admin for places_remember models."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, Memory


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin for CustomUser with avatar_url in list display."""

    list_display = ("username", "email", "first_name", "last_name", "avatar_url")
    list_filter = ("is_staff", "is_superuser", "is_active")


@admin.register(Memory)
class MemoryAdmin(admin.ModelAdmin):
    """Admin for Memory."""

    list_display = ("title", "user", "lat", "lng", "created_at")
    list_filter = ("user",)
    search_fields = ("title", "comment")
