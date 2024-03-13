from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import VideoForm
from .models import Narration
from .utils.email import send_email_test
from .vision.video import VideoAnalyser
from users.forms import PasswordForm


def home_view(request):
    return redirect("website:vision")


# @login_required
def vision_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                video = form.save()
                video_path = video.video_file.url

                # Process video
                analyser = VideoAnalyser(video=video_path, custom_prompt=request.POST.get("prompt"))
                analyser.read_frames()
                narration = analyser.generate_narration()

                # Save Narration to DB
                if narration is not None:
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


# Email Send Test Function
def send_email_view(request):
    send_email_test(
        name="John Elkan",
        message="Why so serious? Testing the email functionality.",
        reply_to="john@gmail.com"
    )
    messages.error(request, "Email sent!")
    return redirect("website:vision")
