# newsletter/tasks.py
from django.core.mail import send_mass_mail
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def send_newsletter_emails(self, messages):
    try:
        send_mass_mail(messages, fail_silently=False)
    except Exception as e:
        self.retry(exc=e, countdown=5)