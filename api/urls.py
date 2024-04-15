from django.urls import path, include
from rest_framework import routers

from .views import NarrationViewSet

app_name = 'api'

router = routers.DefaultRouter()


# API Routes
router.register(r'narrations', NarrationViewSet, 'narrations')


urlpatterns = [
    path('', include(router.urls)),
]
