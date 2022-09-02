from apps.candidates.models import Candidate
from apps.vacancies.models import Vacancy
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

    Methods
    --------------
    render_body(context: dict, candidate=None, vacancy=None)
        the method renders an HTML body that can be then passed to the email
        handler for sending it. it supports HTML, django standard templates
        and custom templates. Read docs on the 'body' attribule for info.
    render_subject(context: dict, candidate=None, vacancy=None)
        same as render_body, but used for rendering

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
        auto_now=True,
    )
    changed_at = models.DateTimeField(
        _("Last updated"),
        auto_now_add=True,
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
            "HTML content (may contain template variables). You can use special "
            "codes that will be substituted with appropriate information. This "
            "template supports Candidates and Vacancies.<br/><br/>"
            "<b>Candidates</b><br/>-----------<br/>"
            "{{cfullname}} stands for candidate's full name<br/>"
            "{{cname}} stands for candidate's firstname<br/>"
            "{{csurname}} stands for candidate's surname<br/>"
            "{{cage}} stands for candidate's age<br/><br/>"
            "<b>Vacancy</b><br/>-----------<br/>"
            "{{vtitle}} stands for vacancy title<br/>"
            "{{vetype}} stands for vacancy employment type<br/>"
            "{{vlocation}} stands for vacancy location<br/>"
            "{{vel}} stands for vacancy level of english<br/>"
            "{{vme}} stands for minimal experience for vacancy<br/>"
            "{{vsd}} stands for vacancy start date<br/>"
            "{{ved}} stands for vacancy end date<br/>"
            "{{vdes}} stands for vacancy description<br/>"
            "{{vsalmin}} stands for vacancy minimal salary<br/>"
            "{{vsalmax}} stands for vacancy maximal salary<br/>"
            "{{vsalcur}} stands for vacancy salary currency<br/>"
            "-----------<br/><br/>You can use your own, which you can later add "
            "while sending emails."
        ),
    )

    def __str__(self) -> str:
        """Return a readable name for the object."""
        return f"{self.name} [{self.subject}]"

    def __repr__(self) -> str:
        """Return a detailed info on the object."""
        return f"<EmailTemplate id={self.id} name='{self.name}'>"

    def render_body(
        self, context: dict, candidate: Candidate = None, vacancy: Vacancy = None
    ) -> str:
        """This method renders body for the message that can be
        later used as HTML attachment for EmailMultiAlternatives.
        """
        return Template(self.body).render(
            Context(context | self._form_keywords(candidate, vacancy))
        )

    def render_subject(
        self, context: dict, candidate: Candidate = None, vacancy: Vacancy = None
    ) -> str:
        """Renders subjects for the email."""
        return Template(self.subject).render(
            Context(context | self._form_keywords(candidate, vacancy))
        )

    def _form_keywords(self, candidate: Candidate = None, vacancy: Vacancy = None) -> dict:
        """Forms keywords if objects were attached to the Template. For each attached
        object a dictionary for context substitution is formed. Read help message
        in 'body' field for more info.
        """
        keywords = {}
        if candidate:
            keywords.update(
                {
                    "cfullname": candidate.full_name,
                    "cname": candidate.name,
                    "csurname": candidate.surname,
                    "cage": candidate.age,
                }
            )
        if vacancy:
            keywords.update(
                {
                    "vtitle": vacancy.title,
                    "vetype": vacancy.type_of_employment,
                    "vlocation": vacancy.location,
                    "vel": vacancy.english_level,
                    "vme": vacancy.min_experience,
                    "vsd": vacancy.start_date,
                    "ved": vacancy.end_date,
                    "vdes": vacancy.description,
                    "vsalmin": vacancy.salary_min,
                    "vsalmax": vacancy.salary_max,
                    "vsalcur": vacancy.salary_currency,
                }
            )
        return keywords
