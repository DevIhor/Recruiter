from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Profile


@receiver(pre_delete, sender=Profile)
def delete_profile_image(sender, instance, **kwargs):
    """
    Must delete profile images from storage here but not in model's `delete()` method because
    when deleting objects from admin panel, django uses `bulk_delete()` on a queryset
    and doesn't call `delete()` method for each instance.
    """
    instance.avatar_image.delete()
