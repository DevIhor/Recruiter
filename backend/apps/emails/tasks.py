import smtplib

from apps.emails.models import EmailLetter
from config.celery import app
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags


@app.task(bind=True, default_retry_delay=2 * 60)
def send_emails(self, email_letter: int, context: dict = None):
    """Celery task to send emails for Candidates."""
    email = EmailLetter.objects.get(id=email_letter)
    if not context:
        context = {}
    candidates = (candidate for candidate in email.recipients.all() if candidate.email)
    template = email.template

    email.mark_in_progress()

    for candidate in candidates:
        try:
            subj = template.render_subject(
                context=context,
                candidate=candidate,
                vacancy=email.vacancy,
                event=email.event,
            )
            msg = template.render_body(
                context=context,
                candidate=candidate,
                vacancy=email.vacancy,
                event=email.event,
            )
            send_mail(
                subject=subj,
                html_message=msg,
                message=strip_tags(msg),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=(candidate.email,),
                fail_silently=False,
            )
        except smtplib.SMTPException as err:
            self.retry(exc=err)

    email.mark_sent()
    email.set_sent_datetime()
