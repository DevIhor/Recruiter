from django.db import models
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _


class EmailTemplate(models.Model):
    """
    This class represents a Templtae for an email. They can be created by Recruiters
    in order to use them for sending emails through EmailLetter. The EmailLetter
    class handles all the functionality regarding sending emails, attaching objects
    etc. EmailTemplate class manages a ...

    Attributes
    --------------
    name : str
        name of the template, only used at Admin Site
    description : str
        description of the template, only used at Admin Site


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
    subject = models.CharField(
        _("Subject"),
        max_length=255,
        help_text=_("HTML content (may contain template variables)."),
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
    body = models.TextField(
        _("HTML template"),
        help_text=_("HTML content (may contain template variables)."),
    )
    keywords = models.JSONField(
        _("Keywords"),
        default=dict,
        blank=True,
    )

    def __str__(self) -> str:
        """ADD"""
        return f"{self.name} [{self.subject}]"

    def __repr__(self) -> str:
        """ADD"""
        return f"<EmailTemplate id={self.id} name='{self.name}' "

    def render_body(self, context: dict):
        """TEST"""
        return Template(self.body).render(Context(self.keywords | context))

    def render_subject(self, context: dict):
        """TEST"""
        return Template(self.body).render(Context(self.keywords | context))
