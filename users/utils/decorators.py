from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def user_is_authenticated(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You have to be logged in to use this feature.")
            return redirect("users:login")

        return view_func(request, *args, **kwargs)
    return _wrapped_view
