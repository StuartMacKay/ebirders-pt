from dateutil.relativedelta import relativedelta

from django import template
from django.db.models import Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ebird.checklists.models import Checklist, Observation

register = template.Library()


@register.inclusion_tag("dashboards/numbers/number.html")
def species_count():
    today = timezone.now().date()
    one_week_ago = today - relativedelta(days=7)
    count = (
        Observation.objects.filter(checklist__date__gt=one_week_ago)
        .values_list("species_id", flat=True)
        .distinct()
        .count()
    )

    return {
        "title": _("Species (plural)"),
        "count": count,
    }


@register.inclusion_tag("dashboards/numbers/number.html")
def checklist_count():
    today = timezone.now().date()
    one_week_ago = today - relativedelta(days=7)
    count = Checklist.objects.filter(date__gt=one_week_ago).count()

    return {
        "title": _("Checklists"),
        "count": count,
    }


@register.inclusion_tag("dashboards/numbers/number.html")
def observer_count():
    today = timezone.now().date()
    one_week_ago = today - relativedelta(days=7)
    count = (
        Checklist.objects.filter(date__gt=one_week_ago)
        .values_list("observer_id", flat=True)
        .distinct()
        .count()
    )

    return {
        "title": _("Observers"),
        "count": count,
    }


@register.inclusion_tag("dashboards/numbers/number.html")
def duration_count():
    today = timezone.now().date()
    one_week_ago = today - relativedelta(days=7)
    total = Checklist.objects.filter(date__gt=one_week_ago).aggregate(Sum("duration"))[
        "duration__sum"
    ]
    return {
        "title": _("Hours"),
        "count": int(total / 60),
    }
