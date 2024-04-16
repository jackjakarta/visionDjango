from django.contrib.auth import get_user_model
from django.db import models

from vision_app.models import CustomModel
from .utils import validate_video_extension

AuthUser = get_user_model()


class Video(CustomModel):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/', validators=[validate_video_extension])

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()


class Audio(CustomModel):
    title = models.CharField(max_length=100, blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()


class Narration(CustomModel):
    text = models.TextField(null=True)
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='narrations',
        related_query_name='narration'
    )
    video = models.OneToOneField(
        Video,
        on_delete=models.CASCADE,
        related_name='videos',
        related_query_name='video'
    )
    audio = models.OneToOneField(
        Audio,
        on_delete=models.SET_NULL,
        related_name='audios',
        related_query_name='audio',
        null=True
    )

    def __str__(self):
        return f"{self.user} - {self.video}"

    def __repr__(self):
        return self.__str__()
