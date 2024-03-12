import os

from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import VideoForm
from .vision.video import VideoAnalyser
from .models import Narration


def home_view(request):
    return redirect("website:vision")


# @login_required
def vision_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                video = form.save()
                video_path = os.path.join(settings.MEDIA_ROOT, str(video.video_file))

                # Process the uploaded video
                analyser = VideoAnalyser(video_path)
                analyser.read_frames()
                narration = analyser.generate_narration()

                # Save Narration to DB
                Narration.objects.create(
                    text=narration,
                    user=request.user,
                    video=video
                )

                return render(request, "website/vision_results.html", {
                    "narration": narration,
                })
        else:
            form = VideoForm()

        return render(request, "website/vision.html", {
            'form': form,
        })
    else:
        return render(request, "website/vision.html")
