from django.contrib import admin
from .models import Audio, Video, Narration


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Narration)
class NarrationAdmin(admin.ModelAdmin):
    pass
