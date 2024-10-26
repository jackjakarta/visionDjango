from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import reverse
from django.template.loader import get_template

from users.utils.constants import ACTIVATION_AVAILABILITY


def send_activation_email(user):
    domain = Site.objects.get_current().domain
    url = reverse("users:activation:activate", args=(user.activation.token,))
    activation_url = f"https://{domain}{url}"
    print(activation_url)

    context = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "activation_url": activation_url,
        "availability": ACTIVATION_AVAILABILITY,
    }

    template = get_template("users/email/activation_email.html")
    content = template.render(context)
    mail = EmailMultiAlternatives(
        subject="Your account has been created.",
        body=content,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    mail.content_subtype = "html"
    mail.send()
