from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def role_required(*allowed):
    """View decorator → 403 redirect to home if session role not in *allowed."""
    def outer(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.session.get("role") not in allowed:
                return redirect(reverse("home"))
            return view(request, *args, **kwargs)
        return wrapper
    return outer
