from django.contrib.auth.models import AbstractUser
from django.db import models

from vision_app.models import CustomModel
from website.utils.constants import COUNTRY_CHOICES
from .managers import AuthUserManager


class AuthUser(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="email",
        max_length=250,
        unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = AuthUserManager()

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.__str__()


class Profile(CustomModel):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default=None, blank=True)
    city = models.CharField("City", max_length=120, blank=True)
    country = models.CharField("Country", choices=COUNTRY_CHOICES, max_length=120, default=None, blank=True)

    def __str__(self):
        return str(self.user)

    def __repr__(self):
        return self.__str__()
