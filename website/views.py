from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from users.utils.decorators import user_is_authenticated
from .audio import ElevenLabsTTS
from .forms import VideoForm
from .models import Narration
from .utils.email import send_email_test
from .utils.save import save_speech_to_db
from .vision.video import VideoAnalyser


def home_view(request):
    return redirect("website:vision")


def vision_view(request):
    if not request.user.is_authenticated:
        return redirect("users:login")

    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        custom_prompt = request.POST.get("prompt")  # Extra field added on template

        if form.is_valid():
            video = form.save()
            video_path = video.video_file.url

            # Process video
            analyser = VideoAnalyser(video=video_path, custom_prompt=custom_prompt)
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
    send_email_test(
        name="John Elk",
        message="Why so serious? Testing the email functionality.",
        reply_to="john@gmail.com"
    )
    messages.success(request, "Email sent!")
    return redirect("website:vision")
