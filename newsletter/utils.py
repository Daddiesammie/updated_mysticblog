# newsletter/utils.py
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives
from contextlib import contextmanager

# newsletter/utils.py
import time
import random

def send_with_exponential_backoff(func, *args, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")

# Usage:
try:
    send_with_exponential_backoff(send_emails_with_connection, emails)
except Exception as e:
    logger.error(f"Failed to send emails after multiple attempts: {str(e)}")

@contextmanager
def get_smtp_connection():
    connection = get_connection(fail_silently=False)
    try:
        connection.open()
        yield connection
    finally:
        connection.close()

def send_emails_with_connection(emails):
    with get_smtp_connection() as connection:
        for email in emails:
            email.connection = connection
            email.send()

# Usage in your signal handler:
@receiver(post_save, sender=BlogPost)
def send_newsletter_notification(sender, instance, created, **kwargs):
    if instance.is_published:
        subscribers = Subscriber.objects.all()
        emails = []
        for subscriber in subscribers:
            context = {
                'post': instance,
                'unsubscribe_url': f"{settings.SITE_URL}/newsletter/unsubscribe/{subscriber.email}/",
                'site_url': settings.SITE_URL,
            }
            html_message = render_to_string('newsletter/email/new_post_notification.html', context)
            plain_message = strip_tags(html_message)
            email = EmailMultiAlternatives(
                subject=f'New Post: {instance.title}',
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email]
            )
            email.attach_alternative(html_message, "text/html")
            emails.append(email)
        
        try:
            send_emails_with_connection(emails)
        except Exception as e:
            logger.error(f"Failed to send emails: {str(e)}")