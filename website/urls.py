from django.urls import path

from .views import home_view, vision_view

app_name = 'website'


urlpatterns = [
    path('', home_view, name='home'),
    path('app/', vision_view, name='vision'),
]
