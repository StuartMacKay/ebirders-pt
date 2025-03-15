from dateutil.relativedelta import relativedelta

from django import template
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ebird.checklists.models import Checklist

register = template.Library()


@register.inclusion_tag("dashboards/tables/big-lists.html")
def big_lists_table():
    today = timezone.now().date()
    one_week_ago = today - relativedelta(days=7)
    checklists = Checklist.objects.filter(date__gt=one_week_ago).order_by(
        "-species_count"
    )[:10]
    return {
        "title": _("Big Lists"),
        "checklists": sorted(list(checklists), key=lambda checklist: checklist.started),
    }
