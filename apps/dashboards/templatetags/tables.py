from dateutil.relativedelta import relativedelta

from django import template
from django.db.models import Count, F, Sum
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


@register.inclusion_tag("dashboards/tables/checklists-submitted.html")
def checklists_submitted_table():
    today = timezone.now().date()
    one_week_ago = today - relativedelta(days=7)

    observers = (
        Checklist.objects.values("observer")
        .annotate(name=F('observer__name'))
        .annotate(count=Count("observer"))
        .filter(date__gt=one_week_ago)
        .filter(complete=True)
        .order_by("-count")
    )[:10]

    return {"observers": observers}


@register.inclusion_tag("dashboards/tables/checklists-duration.html")
def checklists_duration_table():
    today = timezone.now().date()
    one_week_ago = today - relativedelta(days=7)
    observers = (
        Checklist.objects.values("observer")
        .annotate(name=F('observer__name'))
        .annotate(total=Sum("duration"))
        .filter(date__gt=one_week_ago)
        .filter(duration__isnull=False)
        .order_by("-total")
    )[:10]

    for observer in observers:
        observer["hours"] = "%0d" % (observer["total"] / 60)
        observer["minutes"] = "%02d" % (observer["total"] % 60)

    return {"observers": observers}
