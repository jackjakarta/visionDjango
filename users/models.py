import secrets

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from vision_app.models import CustomModel
from website.utils.constants import COUNTRY_CHOICES
from .managers import AuthUserManager
from .utils.constants import ACTIVATION_AVAILABILITY


class AuthUser(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="email",
        max_length=250,
        unique=True
    )
    password = models.CharField(_("password"), max_length=128, null=True, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AuthUserManager()

    def __str__(self):
        return self.email

    def __repr__(self):
        return self.__str__()


AVAILABILITY = {
    ACTIVATION_AVAILABILITY["unit"]: ACTIVATION_AVAILABILITY["value"]
}


class Activation(models.Model):
    user = models.OneToOneField(AuthUser, related_name="activation", on_delete=models.CASCADE)
    token = models.CharField(
        max_length=64,
        null=True,
        unique=True,  # new
        default=None,  # new
    )
    expires_at = models.DateTimeField(
        default=None
    )
    activated_at = models.DateTimeField(default=None, null=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = secrets.token_hex(32)
            self.expires_at = timezone.now() + timezone.timedelta(**AVAILABILITY)
        super().save(*args, **kwargs)


class Profile(CustomModel):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatars/", default=None, blank=True)
    city = models.CharField("City", max_length=120, blank=True)
    country = models.CharField(
        verbose_name="Country",
        choices=COUNTRY_CHOICES,
        max_length=120,
        default=None,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.user)

    def __repr__(self):
        return self.__str__()
