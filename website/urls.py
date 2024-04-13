from django.urls import path

from .views import home_view, vision_view, tts_view, send_email_view, call_api_and_process, get_results

app_name = 'website'


urlpatterns = [
    path('', home_view, name='home'),
    path('app/', vision_view, name='vision'),
    path('tts/<int:narration_id>/', tts_view, name='tts'),
    path('send-mail/', send_email_view, name='email_send'),

    path('process-api/', call_api_and_process, name='process_api'),
    path('results/<uuid:job_id>/', get_results, name='get_results'),
]
