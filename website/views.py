from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse

from users.utils.decorators import user_is_authenticated
from .audio.tts import OpenTTS, ElevenLabsTTS
from .audio.voices import RACHEL
from .forms import VideoForm
from .models import Narration
from .tasks import process_video
from .utils.email import send_email_test
from .utils.moderation import is_harmful


def home_view(request):
    return redirect("website:vision")


@user_is_authenticated
def vision_view(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        custom_prompt = request.POST.get("prompt")  # Extra field added on template

        if is_harmful(custom_prompt):
            messages.error(request, "Your custom prompt contains harmful language!")
            return redirect("website:home")

        if form.is_valid():
            video = form.save()
            video_id = video.pk
            user_id = request.user.pk

            # Process video / Start celery task
            job_id = process_video.delay(video_id, user_id, custom_prompt)

            return render(request, "website/vision_results.html", {
                "api_response": "We are working on it...",
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
        tts_choice = request.POST.get("tts_choice")

        if tts_choice == "elevenlabs":
            tts = ElevenLabsTTS(
                text=narration.text,
                voice=RACHEL
            )
        elif tts_choice == "openai":
            tts = OpenTTS(text=narration.text)
        else:
            tts = None

        tts_str = tts.__str__() if tts is not None else "No model"
        print(tts_str)

        audio_obj = tts.speech_for_narration(narration) if tts is not None else None
        narration.audio = audio_obj
        narration.save()

        if audio_obj is not None:
            messages.success(request, "You have generated a speech file!")
        else:
            messages.error(
                request,
                "There was a problem generating your speech file. Please choose a model and try again."
            )

        return redirect("users:user_narration", narration_id=narration_id)

    else:
        return HttpResponse("Method not allowed", status=405)


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
    else:
        return HttpResponse("Forbidden", status=403)
