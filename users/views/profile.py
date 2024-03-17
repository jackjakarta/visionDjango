from django.contrib import messages
from django.shortcuts import render, redirect

from users.models import Profile
from website.models import Narration


def user_profile(request, user_id):
    if not request.user.is_authenticated:
        messages.error(request, "You have to be logged in to see your profile.")
        return redirect("website:vision")

    try:
        profile = Profile.objects.get(user_id=user_id)
        narrations = Narration.objects.filter(user_id=user_id)
    except Profile.DoesNotExist:
        messages.error(request, "Profile doesn't exist.")
        return redirect("website:home")

    if request.user == profile.user:
        return render(request, "users/profile/user_profile.html", {
            "profile": profile,
            "narrations": narrations,
        })
    else:
        messages.error(request, "This is not your profile!")
        return redirect("website:vision")


def user_narration(request, narration_id):
    if not request.user.is_authenticated:
        messages.error(request, "You have to be logged in to see your profile.")
        return redirect("website:home")

    try:
        narration = Narration.objects.get(pk=narration_id)
    except Narration.DoesNotExist:
        messages.error(request, "Narration doesn't exist.")
        return redirect("website:home")

    if request.user == narration.user:
        return render(request, "users/profile/user_narration.html", {
            "narration": narration,
        })
    else:
        messages.error(request, "You can't access this resource.")
        return redirect("website:home")
