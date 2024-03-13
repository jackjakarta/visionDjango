from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Activation
from .models import Profile
from .utils.email import send_activation_email

AuthUser = get_user_model()


@receiver(post_save, sender=AuthUser)
def create_profile(sender, instance, created, **kwargs):
    print("\nSignals post_save was caught!")
    if created:
        Profile(user=instance).save()
        print("Created profile successfully!")


@receiver(pre_save, sender=AuthUser)
def inactivate_user(sender, instance, **kwargs):
    print("\nSignal pre_save was triggerd!\n")

    if not instance.pk:
        instance.is_active = False
        instance.password = None


@receiver(post_save, sender=AuthUser)
def create_activation(sender, instance, created, **kwargs):
    print("\nSignal post_save was triggerd!\n")
    try:
        with transaction.atomic():
            if created:
                Activation(user=instance).save()
                send_activation_email(instance)
    except ValueError:
        AuthUser.objects.get(pk=instance.id).delete()
