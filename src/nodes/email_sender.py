from pathlib import Path

from src.state import ResearchState
from src.tools.email import (
    send_email,
    EmailAuthenticationError,
    EmailConfigurationError
)


def email_sender(state: ResearchState):

    content = state["email_content"]
    preview_path = Path("newsletter_preview.html")

    preview_path.write_text(
        content,
        encoding="utf-8"
    )

    try:
        send_email(
            receiver_email="p622133@gmail.com",
            content=content
        )
    except EmailConfigurationError as exc:
        print(f"Email skipped: {exc}")
        print(f"Newsletter saved to: {preview_path.resolve()}")
    except EmailAuthenticationError:
        print(
            "Email skipped: SMTP authentication failed. "
            "Set APP_EMAIL_PASSWORD to a valid Gmail app password."
        )
        print(f"Newsletter saved to: {preview_path.resolve()}")

    return {}