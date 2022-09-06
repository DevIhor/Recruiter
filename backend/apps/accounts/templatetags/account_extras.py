from django import template
from django.conf import settings

register = template.Library()


# settings value
@register.simple_tag
def load_option(option, default=None):
    return getattr(settings, option, default)
