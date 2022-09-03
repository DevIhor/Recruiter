from apps.events.models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(
    post_save,
    sender=Event,
    dispatch_uid="calculate_duration_for_event",
)
def calculate_duration_for_event(sender, instance, **kwargs):
    """This calculates duration of the event after each change."""
    new_duration = instance.end_time - instance.start_time
    object = Event.objects.filter(pk=instance.id)
    object.update(duration=new_duration)
