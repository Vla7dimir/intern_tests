"""Social auth pipeline: save user avatar URL to CustomUser."""

from .models import CustomUser


def save_user_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    """Store avatar URL from VK or Google in CustomUser.avatar_url."""
    if not user or not isinstance(user, CustomUser):
        return

    avatar_url = None
    if backend.name == "vk-oauth2":
        avatar_url = response.get("photo_max_orig") or response.get("photo_max")
    elif backend.name == "google-oauth2":
        avatar_url = response.get("picture")

    if avatar_url:
        CustomUser.objects.filter(pk=user.pk).update(avatar_url=avatar_url)
