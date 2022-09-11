from apps.accounts.tasks import send_email_to_user
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django_rest_passwordreset.signals import reset_password_token_created

from .models import Profile


@receiver(pre_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    """
    Must delete profile images from storage here but not in model's `delete()` method because
    when deleting objects from admin panel, django uses `bulk_delete()` on a queryset
    and doesn't call `delete()` method for each instance.
    """
    instance.avatar_image.delete()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """When a token is created, send an email to the user with a confirmation link."""

    email_template_name = "accounts/email/reset_password.html"
    email_context = {
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(reverse("password_reset:reset-password-confirm")),
            reset_password_token.key,
        )
    }
    mail_subject = "Password reset"
    html_message = render_to_string(email_template_name, email_context)
    plain_message = strip_tags(html_message)

    # run celery task to send an email
    send_email_to_user.delay(
        mail_subject, plain_message, [reset_password_token.user.email], html_message
    )
