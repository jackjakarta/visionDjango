from django.contrib.auth.models import AbstractUser
from django.db import models

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
