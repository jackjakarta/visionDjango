from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import Http404, get_object_or_404, redirect, render
from libgravatar import Gravatar

from users.models import Profile
from users.utils.decorators import user_is_authenticated
from website.models import Narration


@user_is_authenticated
def user_profile(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)

    if request.user == profile.user:
        # Avatar from Gravatar
        gravatar_profile = Gravatar(email=profile.user.email)
        avatar_url = gravatar_profile.get_image(size=500)

        # User Narrations
        narrations = Narration.objects.filter(user_id=user_id).order_by("-created_at")

        # Paginator
        paginator = Paginator(narrations, 7)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "users/profile/user_profile.html",
            {
                "profile": profile,
                "avatar_url": avatar_url,
                "page_obj": page_obj,
            },
        )

    else:
        messages.error(request, "This is not your profile!")
        return redirect("website:home")


@user_is_authenticated
def user_narration(request, narration_id):
    narration = get_object_or_404(Narration, pk=narration_id)

    if request.user == narration.user:
        return render(
            request,
            "users/profile/user_narration.html",
            {
                "narration": narration,
            },
        )
    else:
        messages.error(request, "You can't access this resource.")
        return redirect("website:home")


def user_api_key(request, user_id):
    raise Http404
