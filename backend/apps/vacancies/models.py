from apps.accounts.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager


class EmploymentChoices(models.TextChoices):

    FULL_TIME = "FT", _("Full time")
    PART_TIME = "PT", _("Part time")
    OTHER = "OT", _("Other")


class EnglishLevelChoices(models.TextChoices):

    UNKNOWN = "A0", _("Unknown")
    BEGINNER = "A1", _("Beginner")
    ELEMENTARY = "A2", _("Elementary")
    INTERMEDIATE = "B1", _("Intermediate")
    UPPER_INTERMEDIATE = "B2", _("Upper-intermediate")
    ADVANCED = "C1", _("Advanced")
    PROFICIENCY = "C2", _("Proficiency")


class Currency(models.Model):

    currency_title = models.CharField(_("Currency name"), max_length=64)
    currency_code = models.CharField(_("Currency code"), max_length=3)

    def __str__(self):
        return f"{self.currency_code.upper()}: {self.currency_title}"


class ExperienceChoice(models.TextChoices):

    WITHOUT = "0M", _("Without experience")
    MONTH_3 = "3M", _("3 months")
    MONTH_6 = "6M", _("6 months")
    MONTH_9 = "9M", _("9 months")
    YEAR_1 = "1Y", _("1 year")
    YEAR_1_5 = "1.5Y", _("1,5 year")
    YEAR_2 = "2Y", _("2 years")
    YEAR_3 = "3Y", _("3 years")
    YEAR_4 = "4Y", _("4 years")
    YEAR_5 = "5Y", _("5 years")


class Vacancy(models.Model):

    """
    This class represents a Vacancy model, which can be used to create
    vacancirs, and manage them.

    Attributes
    ----------
    title : str
        a title of vacancy
    keywords : str
        a tags with technologies
    type_of_employment : str
        a type of employment
    location : str
        city and country of work, remote work
    english_level : str
        a english_level
    min_experience : float
        a minimum experince by vacancy
    start_date : date
        recruitment start date
    end_date : date
        recruitment end date
    description : str
        about vacancy
    priority : str
        priority in vacancies
    salary_max : int
        maximum salary
    salary_min : int
        minimum salary
    author : str
        author by vacancy
    contact_person : str
        contact person y vacancy
    is_active : boolean
        if vacancy is active
    is_salary_show : boolean
        if we need in vacancy show salary
    """

    title = models.CharField(_("Title"), max_length=64, db_index=True)
    keywords = TaggableManager()
    type_of_employment = models.CharField(
        _("Type of employment"), choices=EmploymentChoices.choices, db_index=True, max_length=32
    )
    location = models.CharField(_("Location"), max_length=128, db_index=True)
    english_level = models.CharField(
        _("English level"), choices=EnglishLevelChoices.choices, db_index=True, max_length=32
    )
    min_experience = models.CharField(
        _("Minimum experience in years"),
        max_length=4,
        choices=ExperienceChoice.choices,
        db_index=True,
        blank=True,
    )
    end_date = models.DateField(_("Recruitment end date"))
    start_date = models.DateField(_("Recruitment start date"))
    description = models.TextField(_("Description"), max_length=2048)
    priority = models.TextField(_("Priority"), max_length=512)
    salary_max = models.IntegerField(_("Maximum salary"), db_index=True)
    salary_min = models.IntegerField(_("Minimum salary"), db_index=True)
    salary_currency = models.ForeignKey(Currency, on_delete=models.DO_NOTHING, db_index=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="vacancy_author")
    contact_person = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="vacancy_contact_person"
    )
    is_active = models.BooleanField(_("Is active"), default=False)
    is_salary_show = models.BooleanField(_("Is salary show"), default=False)

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return self.title

    @property
    def salary(self):
        if self.salary_min == self.salary_max:
            return f"{self.salary_max} {self.salary_currency.currency_code}"
        return f"{self.salary_min}-{self.salary_max} {self.salary_currency.currency_code}"

    @property
    def search_period(self):
        if self.start_date == self.end_date:
            return f"...-{self.end_date.strftime('%Y.%m.%d')}"
        return f"{self.start_date.strftime('%Y.%m.%d')}-{self.end_date.strftime('%Y.%m.%d')}"

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError(
                _("The end date of the search cannot be earlier than the start date!")
            )
        if self.salary_max < self.salary_min:
            raise ValidationError(_("The minimum salary cannot be higher than the maximum!"))