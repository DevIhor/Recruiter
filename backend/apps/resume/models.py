from apps.candidates.models import Candidate
from apps.resume.storages import OverwriteStorage
from apps.vacancies.models import Vacancy
from django.db import models
from django.utils.translation import gettext_lazy as _


def generate_file_path(instance, filename):
    file_path = f"cv/{instance.owner.full_name}/{filename}"
    return file_path


class CurriculumVitae(models.Model):
    """
    This class represents a CV model, which can be used to create
    CV, download files, and manage them.

    Attributes
    ----------
    owner : str
        the candidate to whom the cv belongs
    vacancy : str
        which vacancies the cv has been submitted
    file : filepath
        filepath to cv file
    content : str
        content generated tessaract
    processed_by_tesseract : boolean
        whether the file has been processed by tessaract
    created_at : datetime
        when cv was created
    changed_at : datetime
        when cv was changed
    """

    owner = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="cv_owner",
        verbose_name=_("CV owner"),
    )
    vacancy = models.ManyToManyField(
        Vacancy,
        related_name="cv_vacancies",
        verbose_name=_("Vacancies"),
        blank=True,
    )
    file = models.FileField(
        upload_to=generate_file_path,
        verbose_name=_("CV file"),
        storage=OverwriteStorage(),
    )
    content = models.TextField(_("CV content"), max_length=2048, blank=True)
    processed_by_tesseract = models.BooleanField(_("Processed by tesseract"), default=False)
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
    )
    changed_at = models.DateTimeField(
        _("Last updated"),
        auto_now=True,
    )

    class Meta:
        ordering = ("-id",)

    def __str__(self) -> str:
        """Return CV owner"""
        return f"{self.owner} CV"

    def __repr__(self) -> str:
        """Return debug info for the CV."""
        return f"<CV (id={self.id}) - {self.owner}>"

    @property
    def cv_for_vacancies(self):
        return "; ".join([f"{i.title}" for i in self.vacancy.all()])
