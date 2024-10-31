# newsletter/management/commands/detailed_smtp_test.py
import socket
import smtplib
import ssl
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Detailed SMTP connection test'

    def handle(self, *args, **options):
        self.stdout.write("Starting detailed SMTP test...")

        # Step 1: DNS resolution
        try:
            self.stdout.write("Resolving DNS for smtp.gmail.com...")
            ip = socket.gethostbyname('smtp.gmail.com')
            self.stdout.write(self.style.SUCCESS(f"DNS resolution successful. IP: {ip}"))
        except socket.gaierror as e:
            self.stdout.write(self.style.ERROR(f"DNS resolution failed: {str(e)}"))
            return

        # Step 2: Socket connection
        try:
            self.stdout.write("Attempting socket connection...")
            sock = socket.create_connection((settings.EMAIL_HOST, settings.EMAIL_PORT), timeout=10)
            self.stdout.write(self.style.SUCCESS("Socket connection successful"))
            sock.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Socket connection failed: {str(e)}"))
            return

        # Step 3: SMTP connection
        try:
            self.stdout.write("Initiating SMTP connection...")
            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
            self.stdout.write(self.style.SUCCESS("SMTP connection initiated"))

            self.stdout.write("Sending EHLO...")
            ehlo_response = smtp.ehlo()
            self.stdout.write(self.style.SUCCESS(f"EHLO response: {ehlo_response}"))

            self.stdout.write("Starting TLS...")
            tls_context = ssl.create_default_context()
            starttls_response = smtp.starttls(context=tls_context)
            self.stdout.write(self.style.SUCCESS(f"STARTTLS response: {starttls_response}"))

            self.stdout.write("Sending EHLO again...")
            ehlo_response = smtp.ehlo()
            self.stdout.write(self.style.SUCCESS(f"EHLO response: {ehlo_response}"))

            smtp.quit()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"SMTP connection failed: {str(e)}"))
            return

        # Step 4: SMTP Authentication
        try:
            self.stdout.write("Attempting SMTP authentication...")
            smtp = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10)
            smtp.ehlo()
            smtp.starttls(context=ssl.create_default_context())
            smtp.ehlo()
            smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            self.stdout.write(self.style.SUCCESS("SMTP authentication successful"))
            smtp.quit()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"SMTP authentication failed: {str(e)}"))
            return

        self.stdout.write(self.style.SUCCESS("All tests completed successfully"))