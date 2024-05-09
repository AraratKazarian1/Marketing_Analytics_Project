from combogenius.api.config import HOST, USERNAME, PASSWORD, PORT, MailBody
from ssl import create_default_context
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

def send_email(recipient, subject, html_content):
    # Email Content
    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))

    # SMTP Connection and Sending Email
    with smtplib.SMTP(HOST, PORT) as server:
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.sendmail(USERNAME, recipient, msg.as_string())