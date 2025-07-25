from django import template
from django.template.defaultfilters import floatformat
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter(is_safe=True)
def duration_format(value):
    if value:
        hours = int(value / 60)
        minutes = value % 60

        if hours and minutes:
            result = _("%(hours)dh %(minutes)0dm") % {"hours": hours, "minutes": minutes}
        elif hours and not minutes:
            result = _("%(hours)d") % {"hours": hours}
        else: # not hours and minutes
            if minutes == 1:
                result = _("%(minutes)d min") % {"minutes": minutes}
            else:
                result = _("%(minutes)d mins") % {"minutes": minutes}
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
