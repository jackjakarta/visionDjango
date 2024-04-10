from django.urls import path

from users.views.profile import user_profile

app_name = 'profile'


urlpatterns = [
    path('<int:user_id>/', user_profile, name='user_profile'),
]
