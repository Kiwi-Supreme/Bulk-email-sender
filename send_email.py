import os
import aiosmtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

async def send_email(recipient: str, subject: str, message: str):
    email = EmailMessage()
    email["From"] = os.getenv("EMAIL_SENDER")
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(message)

    await aiosmtplib.send(
        email,
        hostname=os.getenv("EMAIL_HOST"),
        port=int(os.getenv("EMAIL_PORT")),
        start_tls=True,
        username=os.getenv("EMAIL_SENDER"),
        password=os.getenv("EMAIL_PASSWORD"),
    )
