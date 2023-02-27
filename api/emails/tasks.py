# Create your tasks here
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def email_send(subject, message, sender_email, email, html_message):
    # 메세지 보내기
    try:
        send_mail(subject, message, sender_email, email, html_message=html_message)
    except Exception:
        return False

    return True


