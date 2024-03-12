from django.urls import path

from .views import login_user, logout_user

app_name = 'users'


urlpatterns = [
    path('logout/', logout_user, name='logout'),
    path('login/', login_user, name='login'),
]
