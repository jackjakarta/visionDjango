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
    """
    Creates profile for the user on creation.
    """
    print("\nSignals post_save was caught!")

    if created:
        Profile(user=instance).save()
        print("Created profile successfully!")


@receiver(pre_save, sender=AuthUser)
def inactivate_user(instance, **kwargs):
    """
    Inactivate user on creation if it's not a social user.
    """
    is_social_user = (
        hasattr(instance, "is_social_auth") and instance.is_social_auth is True
    )

    if not instance.pk and not is_social_user:
        instance.is_active = False
        instance.password = None


@receiver(post_save, sender=AuthUser)
def create_activation(sender, instance, created, **kwargs):
    """
    Create an Activation object and send an activation email when a new user is created.
    """
    if not isinstance(instance, AuthUser):
        return

    print("!!! Signal post_save was triggered!")
    is_social_user = (
        hasattr(instance, "is_social_auth") and instance.is_social_auth is True
    )

    try:
        with transaction.atomic():
            if created:
                if not is_social_user:
                    Activation(user=instance).save()
                    send_activation_email(instance)
                else:
                    # send_register_user_email(instance)
                    print(f"Sending welcome email to: {instance.email}")
    except ValueError:
        AuthUser.objects.get(pk=instance.id).delete()
