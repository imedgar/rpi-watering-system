# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(sender, receiver, subject, content, output=False):
    message = Mail(
        from_email=sender,
        to_emails=receiver,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        if output:
            print(response.status_code)
            print(response.body)
            print(response.headers)
        return response.status_code
    except Exception as e:
        print(e.message)
