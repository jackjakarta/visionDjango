from django.urls import path

from .views import home_view, vision_view, tts_view, send_email_view, get_vision_results

app_name = "website"


urlpatterns = [
    path("", home_view, name="home"),
    path("app/", vision_view, name="vision"),
    path("tts/<int:narration_id>/", tts_view, name="tts"),
    path("send-mail/", send_email_view, name="email_send"),
    # Celery get results
    path("results/<uuid:job_id>/", get_vision_results, name="get_results"),
]
