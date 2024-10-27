from django.contrib import messages
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.decorators import decorator_from_middleware

from users.forms import PasswordForm
from users.middlewares.activation_middleware import ActivationMiddleware
from users.models import AVAILABILITY, Activation
from users.utils.email import send_activation_email


@decorator_from_middleware(ActivationMiddleware)
def activate_user(request, token):
    activation = get_object_or_404(Activation, token=token)
    user = activation.user

    if request.method == "GET":
        form = PasswordForm(user)
    else:
        form = PasswordForm(user, request.POST)
        if form.is_valid():
            form.save()

            user.is_active = True
            user.save()

            activation.activated_at = timezone.now()
            activation.save()

            messages.success(
                request,
                "Your account has been activated. You can log in into your account.",
            )
            return redirect("website:vision")

    return render(
        request,
        "users/set_password.html",
        {
            "form": form,
            "token": token,
        },
    )


@decorator_from_middleware(ActivationMiddleware)
def reset_token(request, token):
    if request.method == "GET":
        return render(
            request,
            "users/reset_token.html",
            {
                "token": token,
            },
        )

    activation = get_object_or_404(Activation, token=token)
    activation.expires_at = timezone.now() + timezone.timedelta(**AVAILABILITY)
    activation.save()
    send_activation_email(activation.user)

    return HttpResponse(
        "Token has been reset," "Please follow the instructions received on your email"
    )
