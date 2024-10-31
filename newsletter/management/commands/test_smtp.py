# newsletter/management/commands/test_smtp.py
import socket
import smtplib
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Test SMTP connection'

    def handle(self, *args, **options):
        self.stdout.write("Testing SMTP connection...")

        # Test socket connection
        try:
            sock = socket.create_connection((settings.EMAIL_HOST, settings.EMAIL_PORT), timeout=10)
            self.stdout.write(self.style.SUCCESS("Socket connection successful"))
            sock.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Socket connection failed: {str(e)}"))
            return

        # Test SMTP connection
        try:
            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            self.stdout.write(self.style.SUCCESS("SMTP connection successful"))
            smtp.quit()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"SMTP connection failed: {str(e)}"))
            return

        # Test login
        try:
            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            self.stdout.write(self.style.SUCCESS("SMTP login successful"))
            smtp.quit()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"SMTP login failed: {str(e)}"))
            return

        self.stdout.write(self.style.SUCCESS("All tests passed successfully"))