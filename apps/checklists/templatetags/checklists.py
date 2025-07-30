from django import template
from django.template.defaultfilters import floatformat
from django.utils.translation import gettext_lazy as _

from ..forms import Protocol

register = template.Library()


@register.filter(is_safe=True)
def protocol_name(checklist):
    if checklist.protocol_code in Protocol.values:
        result = Protocol(checklist.protocol_code).label
    else:
        result = ""
    return result


@register.filter(is_safe=True)
def distance_format(value):
    if value:
        result = _("%(distance)s km") % {"distance": floatformat(value)}
    else:
        result = ""
    return result


@register.filter(is_safe=True)
def area_format(value):
    if value:
        result = _("%(area)s ha") % {"area": floatformat(value)}
    else:
        result = ""
    return result
