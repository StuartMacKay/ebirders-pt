from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def get_contents(notification, language_code):
    if "contents" in notification.data:
        if language_code in notification.data["contents"]:
            return mark_safe(notification.data["contents"][language_code])
    return mark_safe(notification.contents)
