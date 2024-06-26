from django.urls import path, include

from users.views import login_user, logout_user, register_view, get_api_key
from users.views.profile import user_narration

app_name = 'users'


urlpatterns = [
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('register/', register_view, name='register'),
    path('activation/', include('users.urls.activation')),
    path('social-auth/', include('social_django.urls')),
    path('get-api-key/', get_api_key, name='get_api_key'),

    path('profile/', include('users.urls.profile')),
    path('narration/<int:narration_id>/', user_narration, name='user_narration'),
]
