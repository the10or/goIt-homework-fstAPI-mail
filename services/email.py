from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from config import (MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM,
                    MAIL_PORT, MAIL_SERVER, MAIL_FROM_NAME, TEMPLATE_FOLDER)

from services.auth import auth_service

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=TEMPLATE_FOLDER
)


async def send_email(email: EmailStr, host: str):
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Verify your email",
            recipients=[email],
            template_body={
                "host": host,
                "username": email,
                "token": token_verification
            },
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_template.html")

    except ConnectionErrors as err:
        print(err)
