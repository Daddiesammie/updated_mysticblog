# newsletter/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from blog.models import BlogPost
from .models import Subscriber
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=BlogPost)
def send_newsletter_notification(sender, instance, created, **kwargs):
    print(f"Signal triggered for BlogPost: {instance.title}")  # Basic print for immediate feedback
    logger.info(f"Signal triggered for BlogPost: {instance.title}")
    
    # Only send emails when the post is published
    if instance.is_published:
        print(f"Post is published, preparing to send emails...")  # Additional feedback
        subscribers = Subscriber.objects.all()
        subscriber_count = subscribers.count()
        print(f"Found {subscriber_count} subscribers")  # Check subscriber count
        
        if subscriber_count == 0:
            print("No subscribers found!")
            return
            
        try:
            # Prepare mass emails
            messages = []
            for subscriber in subscribers:
                print(f"Preparing email for: {subscriber.email}")  # Track email preparation
                
                # Render HTML email template
                context = {
                    'post': instance,
                    'unsubscribe_url': f"{settings.SITE_URL}/newsletter/unsubscribe/{subscriber.email}/",
                    'site_url': settings.SITE_URL,
                }
                
                html_message = render_to_string('newsletter/email/new_post_notification.html', context)
                plain_message = strip_tags(html_message)
                
                messages.append((
                    f'New Post: {instance.title}',  # Subject
                    plain_message,  # Plain text message
                    settings.DEFAULT_FROM_EMAIL,  # From email
                    [subscriber.email],  # To email
                ))
            
            # Send mass emails
            print("Attempting to send emails...")  # Track sending attempt
            send_mass_mail(messages, fail_silently=False)
            print("Emails sent successfully!")  # Confirm sending
            
        except Exception as e:
            print(f"Error sending emails: {str(e)}")  # Print any errors
            logger.error(f"Error sending emails: {str(e)}")