from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from libgravatar import Gravatar
from users.models import Profile
from users.utils.decorators import user_is_authenticated
from website.models import Narration


@user_is_authenticated
def user_profile(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    narrations = Narration.objects.filter(user_id=user_id).order_by("-created_at")

    if request.user == profile.user:
        gravatar_profile = Gravatar(email=profile.user.email)
        avatar_url = gravatar_profile.get_image(size=500)

        return render(request, "users/profile/user_profile.html", {
            "profile": profile,
            "narrations": narrations,
            "avatar_url": avatar_url,
        })
    else:
        messages.error(request, "This is not your profile!")
        return redirect("website:home")


@user_is_authenticated
def user_narration(request, narration_id):
    narration = get_object_or_404(Narration, pk=narration_id)

    if request.user == narration.user:
        return render(request, "users/profile/user_narration.html", {
            "narration": narration,
        })
    else:
        messages.error(request, "You can't access this resource.")
        return redirect("website:home")
