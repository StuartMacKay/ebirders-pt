from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def get_reason(observation, language_code):
    if "reason" in observation.data:
        if language_code in observation.data["reason"]:
            return mark_safe(observation.data["reason"][language_code])
    return mark_safe(observation.reason)
