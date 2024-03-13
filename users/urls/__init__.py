from django.urls import path, include

from users.views import login_user, logout_user, register_view

app_name = 'users'


urlpatterns = [
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
    path('register/', register_view, name='register'),
    path('activation/', include('users.urls.activation')),

    path('<int:user_id>/', include('users.urls.profile')),
]
