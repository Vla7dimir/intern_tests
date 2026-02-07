"""Views for places_remember app."""

from django.conf import settings
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import MemoryForm
from .models import Memory

User = get_user_model()


def index(request):
    """Show welcome page or user's memory list."""
    if not request.user.is_authenticated:
        vk_configured = bool(
            getattr(settings, "SOCIAL_AUTH_VK_OAUTH2_KEY", "")
        )
        google_configured = bool(
            getattr(settings, "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "")
        )
        return render(
            request,
            "places_remember/index.html",
            {
                "vk_configured": vk_configured,
                "google_configured": google_configured,
                "debug": settings.DEBUG,
            },
        )
    memories = Memory.objects.filter(user=request.user)
    name = request.user.get_full_name() or request.user.username
    avatar_url = getattr(request.user, "avatar_url", None) or ""
    return render(
        request,
        "places_remember/memory_list.html",
        {
            "memory_list": memories,
            "name": name,
            "avatar_url": avatar_url,
        },
    )


@require_http_methods(["GET", "POST"])
def add_memory(request):
    """Show form to add a memory or save it."""
    if not request.user.is_authenticated:
        return redirect("places_remember:index")
    if request.method == "POST":
        form = MemoryForm(request.POST)
        if form.is_valid():
            Memory.objects.create(
                user=request.user,
                title=form.cleaned_data["title"],
                comment=form.cleaned_data["comment"],
                lat=form.cleaned_data["lat"],
                lng=form.cleaned_data["lng"],
            )
            return redirect("places_remember:index")
    else:
        form = MemoryForm(initial={"lat": 55.7558, "lng": 37.6173})
    return render(request, "places_remember/form.html", {"form": form})


@require_GET
def logout_view(request):
    """Log out and redirect to welcome page."""
    auth_logout(request)
    return redirect("places_remember:index")


@require_GET
def dev_login(request):
    """
    Log in as test user without OAuth. Only available when DEBUG=True.
    """
    if not settings.DEBUG:
        return redirect("places_remember:index")
    user, _ = User.objects.get_or_create(
        username="devuser",
        defaults={
            "first_name": "Тестовый",
            "last_name": "Пользователь",
        },
    )
    backend = "django.contrib.auth.backends.ModelBackend"
    auth_login(request, user, backend=backend)
    return redirect("places_remember:index")
