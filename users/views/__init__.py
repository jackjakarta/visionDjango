from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.shortcuts import redirect, render

from users.forms import RegisterForm


def login_user(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect("website:vision")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in.")
            return redirect("website:vision")
        else:
            messages.error(request, "There was a problem logging you in. Try again.")
            return redirect("users:login")

    return render(request, "users/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect("website:home")


def register_view(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already registered and logged in.")
        return redirect("website:vision")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "You have registered successfully!")
            return redirect("website:vision")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def get_api_key(request):
    raise Http404
