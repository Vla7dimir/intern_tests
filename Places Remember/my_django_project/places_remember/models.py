"""Models for places_remember app: CustomUser and Memory."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """User model with optional avatar URL from social auth."""

    avatar_url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.get_full_name() or self.username


class Memory(models.Model):
    """User's memory of a place: title, comment, coordinates."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="memories",
    )
    title = models.CharField(max_length=200)
    comment = models.TextField(max_length=1000)
    lat = models.FloatField()
    lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "memory"
        verbose_name_plural = "memories"

    def __str__(self):
        return self.title
