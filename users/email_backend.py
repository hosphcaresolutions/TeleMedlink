import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()
import sendgrid
from sendgrid.helpers.mail import Mail
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings


class SendGridEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
        num_sent = 0
        for message in email_messages:
            mail = Mail(
                from_email=message.from_email,
                to_emails=message.to,
                subject=message.subject,
                plain_text_content=message.body,
                html_content=message.alternatives[0][0] if message.alternatives else None
            )
            try:
                response = sg.send(mail)
                if 200 <= response.status_code < 300:
                    num_sent += 1
            except Exception as e:
                if not self.fail_silently:
                    raise e
        return num_sent
