from typing import List
from django.conf import settings
from django.core.mail import send_mail


def send_email(
    subject: str,
    message: str,
    recipient_list: List[str],
    fail_silently: bool = False,
    html_message: str | None = None,
) -> int:
    """
    Send an email using the configured email backend.
    """
    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        html_message=html_message,
    )
