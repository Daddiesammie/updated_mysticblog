# newsletter/management/commands/test_mailhog.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email sending with MailHog'

    def handle(self, *args, **options):
        subject = 'Test email from Django'
        message = 'This is a test email sent from Django using MailHog.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['test@example.com']

        try:
            send_mail(subject, message, from_email, recipient_list)
            self.stdout.write(self.style.SUCCESS('Test email sent successfully. Check MailHog web interface.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send test email: {str(e)}'))