from django.apps import AppConfig


class CurriculumVitaeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.resume"

    # def ready(self):
    #    from . import tasks  # noqa: F401
