from django.urls import path

from users.views.activation import activate_user, reset_token

app_name = "activation"

urlpatterns = [
    path("activate/<str:token>/", activate_user, name="activate"),
    path("reset-token/<str:token>/", reset_token, name="reset_token"),
]
