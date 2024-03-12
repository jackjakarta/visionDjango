from django.db import models
from django.contrib.auth import get_user_model
from vision_app.models import CustomModel

AuthUser = get_user_model()


class Video(CustomModel):
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()


class Narration(CustomModel):
    text = models.TextField()
    user = models.ForeignKey(
        AuthUser,
        on_delete=models.CASCADE,
        related_name='narrations',
        related_query_name='narration'
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name='videos',
        related_query_name='video'
    )

    def __str__(self):
        return f"{self.user} - {self.video}"

    def __repr__(self):
        return self.__str__()
