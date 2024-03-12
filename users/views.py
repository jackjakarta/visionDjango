from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get("password")

            # Authenticate
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in.")
                return redirect("website:vision")
            else:
                messages.error(request, "There was a problem logging you in.")
                return redirect("website:vision")
    else:
        messages.error(request, "You are already logged in.")
        return redirect("website:vision")


def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out.")
    return redirect("website:home")
