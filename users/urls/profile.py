from django.urls import path, include

from users.views.profile import user_profile, user_narration

app_name = 'profile'


urlpatterns = [
    path('profile/', user_profile, name='user_profile'),
]
