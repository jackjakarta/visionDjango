from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from users.utils.decorators import user_is_authenticated
from .audio import ElevenLabsTTS
from .forms import VideoForm
from .models import Narration
from .tasks import process_data
from .utils.email import send_email_test
from .utils.save import save_speech_to_db
from .vision.video import VideoAnalyser


def home_view(request):
    return redirect("website:vision")


@user_is_authenticated
def vision_view(request):
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
    if request.user.is_superuser:
        send_email_test(
            name="John Elk",
            message="Why so serious? Testing the email functionality.",
            reply_to="john@gmail.com"
        )
        messages.success(request, "Email sent!")
        return redirect("website:vision")


def call_api_and_process(request):
    job_id = process_data.delay("animal")

    # return JsonResponse({'status': 'success', 'job_id': job_id.id})
    return render(request, "website/async.html", {
        "job_id": job_id.id,
    })


def get_results(request, job_id):
    result = cache.get(job_id)

    if result is not None:
        return render(request, "website/async_result.html", {
            "joke": result,
        })
        # return JsonResponse({'status': 'success', 'data': result})
    else:
        # return JsonResponse({'status': 'processing', 'message': 'Results not ready yet'})
        return render(request, "website/async_result.html", {
            "joke": "Results not ready yet."
        })
