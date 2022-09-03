from django.apps import AppConfig


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.events"

    def ready(self) -> None:
        """Explicitly set up signals."""
        from apps.events import signals  # noqa
