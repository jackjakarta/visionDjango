from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404

from users.utils.decorators import user_is_authenticated
from .audio import ElevenLabsTTS
from .forms import VideoForm
from .models import Narration
from .tasks import process_video
from .utils.email import send_email_test
from .utils.save import save_speech_to_db


def home_view(request):
    return redirect("website:vision")


@user_is_authenticated
def vision_view(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        custom_prompt = request.POST.get("prompt")  # Extra field added on template

        if form.is_valid():
            video = form.save()
            video_id = video.pk  # 'video' is an instance of the Video model
            user_id = request.user.pk

            # Process video
            job_id = process_video.delay(video_id, user_id, custom_prompt)

            return render(request, "website/vision_results.html", {
                "api_response": "We are still working on it...",
                "job_id": job_id,
                "refresh_button": True,
            })
    else:
        form = VideoForm()

    return render(request, "website/vision.html", {
        'form': form,
    })


@user_is_authenticated
def get_vision_results(request, job_id):
    result = cache.get(job_id)

    if result is not None:
        messages.success(request, "Your narration is ready.")
        return render(request, "website/vision_results.html", {
            "api_response": result,
            "refresh_button": False,
        })
    else:
        return render(request, "website/vision_results.html", {
            "api_response": "We are still working on it...",
            "job_id": job_id,
            "refresh_button": True,
        })


@user_is_authenticated
def tts_view(request, narration_id):
    narration = get_object_or_404(Narration, pk=narration_id)

    if not request.user == narration.user:
        messages.error(request, "This is not your narration!")
        return redirect("website:home")

    if request.method == "POST":
        tts = ElevenLabsTTS(
            text=str(narration.text),
            voice="21m00Tcm4TlvDq8ikWAM"
        )

        audio_file = tts.generate()
        audio_obj = save_speech_to_db(narration, audio_file)
        narration.audio = audio_obj

        narration.save()

        messages.success(request, "You have generated a speech file!")
        return redirect("users:user_narration", narration_id=narration_id)


# Email Send Test Function
def send_email_view(request):
    if request.user.is_superuser:
        send_email_test(
            name="John Elk",
            message="Why so serious? Testing the email functionality.",
            reply_to="john@gmail.com"
        )
        messages.success(request, "Email sent!")
        return redirect("website:vision")
