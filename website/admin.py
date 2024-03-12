from django.contrib import admin
from .models import Video, Narration


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Narration)
class NarrationAdmin(admin.ModelAdmin):
    pass
