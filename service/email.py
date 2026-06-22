import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from core.config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD


def send_otp_email(email: str, otp: str):

    message = MIMEMultipart()

    message["From"] = EMAIL_USER
    message["To"] = email
    message["Subject"] = "Password Reset OTP"

    body = f"""
Your OTP is: {otp}

This OTP will expire in 10 minutes.

If you did not request this password reset,
please ignore this email.
"""

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(EMAIL_HOST, int(EMAIL_PORT)) as server:

        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASSWORD)

        server.send_message(message)
