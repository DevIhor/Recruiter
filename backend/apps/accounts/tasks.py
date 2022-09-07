import smtplib

from config.celery import app
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

UserModel = get_user_model()


@app.task(bind=True, default_retry_delay=1 * 60)
def send_verification_email(self, user_id: int) -> None:
    """Celery task to send account activation link to user's email address."""

    user = UserModel.objects.get(id=user_id)
    confirmation_token = default_token_generator.make_token(user)

    email_template_name = "accounts/email/confirm_email.html"
    email_context = {
        "user_id": user_id,
        "token": confirmation_token,
    }
    mail_subject = "Activate your account"
    html_message = render_to_string(email_template_name, email_context)
    plain_message = strip_tags(html_message)

    try:
        send_mail(
            subject=mail_subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except smtplib.SMTPException as ex:
        self.retry(exc=ex)
