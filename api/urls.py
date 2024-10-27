from django.urls import include, path
from rest_framework import routers

from .viewsets import NarrationViewSet, tts_create

app_name = "api"


# API Routes
router = routers.DefaultRouter()
router.register(r"narrations", NarrationViewSet, "narrations")


urlpatterns = [
    path("", include(router.urls)),
    path("tts/", tts_create, name="tts_api"),
]
