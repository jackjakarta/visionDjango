from django.conf import settings
from django.core.mail import send_mail


def send_email_test(name, message, reply_to):
    subject = f"New Contact Form Entry ({reply_to})"
    user_message = f"Reply To: {reply_to}\nName: {name}\n\n{message}"

    send_mail(
        subject=subject,
        message=user_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["al.termure@gmail.com"]
    )
