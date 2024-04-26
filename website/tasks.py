from celery import shared_task, current_task
from django.contrib.auth import get_user_model
from django.core.cache import cache

from .models import Narration, Video
from .vision.video import VideoAnalyser

AuthUser = get_user_model()


@shared_task
def process_video(video_id, user_id, custom_prompt):
    video = Video.objects.get(pk=video_id)
    user = AuthUser.objects.get(pk=user_id)

    job_id = current_task.request.id

    analyser = VideoAnalyser(video=video.video_file.url, custom_prompt=custom_prompt)
    narration = analyser.generate_narration()

    if narration:
        Narration.objects.create(text=narration, user=user, video=video)

    cache.set(job_id, narration, timeout=3600)

    return job_id
