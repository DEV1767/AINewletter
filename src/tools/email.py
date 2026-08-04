import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailConfigurationError(ValueError):
    pass


class EmailAuthenticationError(smtplib.SMTPAuthenticationError):
    pass


def send_email(receiver_email: str, content: str):

    sender_email = os.getenv("APP_EMAIL")
    app_password = os.getenv("APP_EMAIL_PASSWORD")

    if not sender_email or not app_password:
        raise EmailConfigurationError(
            "APP_EMAIL and APP_EMAIL_PASSWORD must be set to send email."
        )

    message = MIMEMultipart("alternative")

    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "AI Research Weekly"

    html_part = MIMEText(
        content,
        "html"
    )

    message.attach(html_part)

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        try:
            server.login(
                sender_email,
                app_password
            )
        except smtplib.SMTPAuthenticationError as exc:
            raise EmailAuthenticationError(
                exc.smtp_code,
                b"Email authentication failed. "
                b"Use a valid Gmail app password in APP_EMAIL_PASSWORD."
            ) from exc

        server.sendmail(
            sender_email,
            receiver_email,
            message.as_string()
        )

    print("Newsletter sent successfully")