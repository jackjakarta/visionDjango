import requests
from celery import shared_task
from django.core.cache import cache

from .models import Narration
from .vision.video import VideoAnalyser


@shared_task(bind=True)
def process_data(self, data):
    job_id = self.request.id

    # API Call
    response = requests.get(f'https://api.chucknorris.io/jokes/random?category={data}')
    data = response.json()
    joke = data.get("value")

    # Store result in cache with a timeout of 1 hour
    cache.set(job_id, joke, timeout=3600)

    return job_id


@shared_task
def process_video(video_id, user_id, custom_prompt):
    from .models import Video
    video = Video.objects.get(id=video_id)
    video_path = video.video_file.url
    analyser = VideoAnalyser(video=video_path, custom_prompt=custom_prompt)
    analyser.read_frames()
    narration = analyser.generate_narration()

    if narration is not None:
        Narration.objects.create(
            text=narration,
            user_id=user_id,
            video=video
        )
    return narration
