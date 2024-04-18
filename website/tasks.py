from celery import shared_task, current_task
from django.contrib.auth import get_user_model
from django.core.cache import cache

from .models import Narration
from .vision.video import VideoAnalyser


# @shared_task(bind=True)
# def process_data(self, data):
#     job_id = self.request.id
#
#     # API Call
#     response = requests.get(f'https://api.chucknorris.io/jokes/random?category={data}')
#     data = response.json()
#     joke = data.get("value")
#
#     # Store result in cache with a timeout of 1 hour
#     cache.set(job_id, joke, timeout=3600)
#
#     return job_id


@shared_task
def process_video(video_id, user_id, custom_prompt):
    from .models import Video  # Import models inside the task to avoid circular imports
    AuthUser = get_user_model()  # NOQA

    video = Video.objects.get(pk=video_id)
    user = AuthUser.objects.get(pk=user_id)

    job_id = current_task.request.id

    analyser = VideoAnalyser(video=video.video_file.url, custom_prompt=custom_prompt)  # Adjust accordingly
    narration = analyser.generate_narration()

    if narration:
        Narration.objects.create(text=narration, user=user, video=video)

    cache.set(job_id, narration, timeout=3600)

    return job_id
