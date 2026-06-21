from core.email import send_email

send_email(
    to_email="kanhaathakkar001@gmail.com",
    subject="SMTP Test",
    body="Hello from FastAPI SMTP"
)

print("Email sent successfully")