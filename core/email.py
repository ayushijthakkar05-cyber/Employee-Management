import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD


def send_email(to_email: str, subject: str, body: str):

    message = MIMEMultipart()

    message["From"] = EMAIL_USER
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP(EMAIL_HOST, int(EMAIL_PORT))

    server.starttls()

    server.login(EMAIL_USER, EMAIL_PASSWORD)

    server.sendmail(EMAIL_USER, to_email, message.as_string())

    server.quit()
