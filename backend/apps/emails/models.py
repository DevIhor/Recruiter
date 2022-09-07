from datetime import datetime

from apps.candidates.models import Candidate
from apps.events.models import Event
from apps.vacancies.models import Vacancy
from base.models import EmailStatus
from django.db import models
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _


class EmailTemplate(models.Model):
    """
    This class represents a Template for an email. It can be created by Recruiters
    in order to use them for sending emails through EmailLetter. The EmailLetter
    class handles all the functionality regarding sending emails, attaching objects
    etc. EmailTemplate class manages only a template which is stored in 'body' as
    a plain text, which although contains and understands both html tags and django
    templates. It also has its' own template words.

    Attributes
    --------------
    name : str
        name of the template, only used at Admin Site
    description : str
        description of the template, only used at Admin Site
    created_at : datetime
        time of creation of the template
    changed_at : datetime
        time of the last change to the template
    body : str
        template body text, which is then rendered into HTML email
    subject : str
        template subject text, which is then rendered into subject
    author : Profile
        author of the template

    Methods
    --------------
    render_body(context: dict, candidate=None, vacancy=None)
        the method renders an HTML body that can be then passed to the email
        handler for sending it. it supports HTML, django standard templates
        and custom templates. Read docs on the 'body' attribule for info.
    render_subject(context: dict, candidate=None, vacancy=None)
        same as render_body, but used for rendering a subject

    """

    name = models.CharField(
        _("Template name"),
        max_length=255,
        db_index=True,
    )
    description = models.TextField(
        _("Description"),
        max_length=500,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    changed_at = models.DateTimeField(
        _("Last updated"),
        auto_now=True,
    )
    subject = models.CharField(
        _("Subject"),
        max_length=255,
        help_text=_("HTML content (may contain template variables, read body docs)."),
        blank=True,
        null=True,
    )
    body = models.TextField(
        _("HTML template"),
        help_text=_(
            "This template can support adding Event/Candidate/Vacancy info through "
            "usage of special tags. Just inserst a {{TAG_NAME}} in the template and "
            "it will be substituted for the appropriate info.<br/><br/>"
            "<b><h3>Available tags:</h3></b><br/>"
            "<b>Candidates</b>: name ({{candidate_name}}), surname ({{candidate_surname}}), "
            "full name ({{candidate_fullname}}), age ({{candidate_age}}).<br/><br/>"
            "<b>Vacancies</b>: title ({{vacancy_title}}), type ({{vacancy_etype}}), "
            "location ({{vacancy_location}}), level of Englisg ({{vacancy_el}}), <br/>"
            "minimal experience ({{vacancy_me}}), start date ({{vacancy_sd}}), end date "
            "({{vacancy_ed}}), description ({{vacancy_des}}), minimal salary "
            "({{vacancy_salmin}}), <br/> maximal salary ({{vacancy_salmax}}), salary currency "
            "({{vacancy_salcur}}).<br/><br/><b>Events</b>: title ({{event_title}})"
            ", description ({{event_description}}), type ({{event_type}}), start time"
            " ({{event_st}}),<br/> end time ({{event_et}}), duration ({{event_duration}})."
        ),
    )

    author = models.ForeignKey(
        "accounts.Profile",
        related_name="email_templates",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        """Return a readable name for the object."""
        return f"{self.name} [{self.subject}]"

    def __repr__(self) -> str:
        """Return a detailed info on the object."""
        return f"<EmailTemplate id={self.id} name='{self.name}'>"

    def render_body(
        self,
        context: dict,
        candidate: Candidate = None,
        vacancy: Vacancy = None,
        event: Event = None,
    ) -> str:
        """This method renders body for the message that can be
        later used as HTML attachment for EmailMultiAlternatives.
        """
        return Template(self.body).render(
            Context(context | self._generate_keywords(candidate, vacancy, event))
        )

    def render_subject(
        self,
        context: dict,
        candidate: Candidate = None,
        vacancy: Vacancy = None,
        event: Event = None,
    ) -> str:
        """Renders subjects for the email."""
        return Template(self.subject).render(
            Context(context | self._generate_keywords(candidate, vacancy, event))
        )

    def _generate_keywords(
        self,
        candidate: Candidate = None,
        vacancy: Vacancy = None,
        event: Event = None,
    ) -> dict:
        """Forms keywords if objects were attached to the Template. For each attached
        object a dictionary for context substitution is formed. Read help message
        in 'body' field for more info.
        """
        keywords = {}
        if candidate:
            keywords.update(
                {
                    "candidate_fullname": candidate.full_name,
                    "candidate_name": candidate.name,
                    "candidate_surname": candidate.surname,
                    "candidate_age": candidate.age,
                }
            )
        if vacancy:
            keywords.update(
                {
                    "vacancy_title": vacancy.title,
                    "vacancy_etype": vacancy.type_of_employment,
                    "vacancy_location": vacancy.location,
                    "vacancy_el": vacancy.english_level,
                    "vacancy_me": vacancy.min_experience,
                    "vacancy_sd": vacancy.start_date,
                    "vacancy_ed": vacancy.end_date,
                    "vacancy_des": vacancy.description,
                    "vacancy_salmin": vacancy.salary_min,
                    "vacancy_salmax": vacancy.salary_max,
                    "vacancy_salcur": vacancy.salary_currency,
                }
            )
        if event:
            keywords.update(
                {
                    "event_title": event.title,
                    "event_description": event.description,
                    "event_type": event.type,
                    "event_st": event.start_time,
                    "event_et": event.end_time,
                    "event_duration": event.duration,
                }
            )
        return keywords


class EmailLetter(models.Model):
    """
    Recruiter should be able to generate an email letter from email template,
    attaching some object (or custom dictionary, or many objects) with data
    (that should be replaced) to template.

    Attributes
    --------------
    name : str
        name of the letter, only used at Admin Site
    template : EmailTemplate
        template, used for rendering
    status : int
        status code of a letter
    created_at : datetime
        time of creation of the letter
    changed_at : datetime
        time of the last change to the letter
    sent_at : datetime
        time of when the letter was sent
    event : Event
        event for template data
    vacancy : Vacancy
        vacancy for template data
    recipients : Candidate
        recipints of the letter, will silently ignore candidates without email

    """

    name = models.CharField(
        _("Letter Name"),
        max_length=100,
    )
    template = models.ForeignKey(
        to=EmailTemplate,
        related_name="emails",
        verbose_name=_("Template"),
        on_delete=models.CASCADE,
    )
    status = models.IntegerField(
        _("Email Status"),
        choices=EmailStatus.choices,
        default=0,
    )
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    changed_at = models.DateTimeField(
        _("Last updated"),
        auto_now=True,
    )
    sent_at = models.DateTimeField(
        _("Sent at"),
        null=True,
    )
    event = models.ForeignKey(
        to=Event,
        verbose_name=_("Associated Event"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    vacancy = models.ForeignKey(
        to=Vacancy,
        verbose_name=_("Associated Vacancy"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    recipients = models.ManyToManyField(
        to=Candidate,
        verbose_name=_("Recipients"),
    )

    @property
    def sent_time(self) -> str:
        if self.sent_at:
            return self.sent_at
        return "Not available"

    def mark_in_progress(self):
        """Mark as 'In Progress'."""
        self.status = EmailStatus.IN_PROCESS
        self.save(update_fields=["status"])

    def mark_sent(self):
        """Mark as 'Sent'."""
        self.status = EmailStatus.SENT
        self.save(update_fields=["status"])

    def set_sent_datetime(self):
        """Set date and time of sending the email."""
        self.sent_at = datetime.now()
        self.save(update_fields=["sent_at"])
