from django.contrib import messages
from django.shortcuts import render, redirect

from users.models import Profile
from website.models import Narration


def user_profile(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request, "You have to be logged in to see your profile.")
        return redirect("website:vision")

    profile = Profile.objects.get(user_id=user_id)
    narrations = Narration.objects.filter(user_id=user_id)

    if request.user == profile.user:
        return render(request, "users/user_profile.html", {
            "profile": profile,
            "narrations": narrations,
        })
    else:
        messages.error(request, "This is not your profile!")
        return redirect("website:vision")
