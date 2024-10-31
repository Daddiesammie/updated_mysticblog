# newsletter/management/commands/test_email.py
from django.core.management.base import BaseCommand
from newsletter.utils import test_email_configuration

class Command(BaseCommand):
    help = 'Test email configuration'

    def handle(self, *args, **options):
        success, message = test_email_configuration()
        if success:
            self.stdout.write(self.style.SUCCESS(message))
        else:
            self.stdout.write(self.style.ERROR(message))