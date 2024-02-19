from django.conf import settings
from django.core.mail import send_mail

def sendEmail(messgae, recipients=None):
    send_mail(
        subject='Notification from RentApp',
        message=messgae,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients,
        fail_silently=False,
    )


