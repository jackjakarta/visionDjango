from django.urls import path, include
from rest_framework import routers

from .viewsets import NarrationsViewSet, tts_create

app_name = 'api'


# API Routes
router = routers.DefaultRouter()
router.register(r'narrations', NarrationsViewSet, 'narrations')


urlpatterns = [
    path('', include(router.urls)),
    path('tts/', tts_create, name='tts_api'),
]
