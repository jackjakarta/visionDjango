from django.urls import path

from users.views.profile import user_api_key, user_profile

app_name = "profile"


urlpatterns = [
    path("<int:user_id>/", user_profile, name="user_profile"),
    path("<int:user_id>/api-key/", user_api_key, name="user_api_key"),
]
