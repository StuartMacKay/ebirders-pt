import logging

from django import template
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from ebird.api.data.models import Checklist, Observation

register = template.Library()
log = logging.getLogger(__name__)


@register.inclusion_tag("news/numbers/number.html")
def species_count(start, finish, country=None, state=None, county=None):
    filters = {
        "published": True,
        "species__category": "species",
        "date__gte": start,
        "date__lte": finish,
    }

    if country:
        filters["country__in"] = country
    if state:
        filters["state__in"] = state
    if county:
        filters["county__in"] = county

    count = (
        Observation.objects.filter(**filters)
        .values_list("species_id", flat=True)
        .distinct()
        .count()
    )

    return {
        "title": _("Species seen"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def checklist_count(start, finish, country=None, state=None, county=None):
    filters = {
        "published": True,
        "date__gte": start,
        "date__lte": finish,
    }

    if country:
        filters["country__in"] = country
    if state:
        filters["state__in"] = state
    if county:
        filters["county__in"] = county

    return {
        "title": _("Checklists submitted"),
        "count": Checklist.objects.filter(**filters).count(),
    }


@register.inclusion_tag("news/numbers/number.html")
def observer_count(start, finish, country=None, state=None, county=None):
    filters = {
        "published": True,
        "date__gte": start,
        "date__lte": finish,
    }

    if country:
        filters["country__in"] = country
    if state:
        filters["state__in"] = state
    if county:
        filters["county__in"] = county

    queryset = Checklist.objects.filter(**filters)

    count = queryset.values_list("observer_id", flat=True).distinct().count()

    return {
        "title": _("Birders"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def duration_count(start, finish, country=None, state=None, county=None):
    filters = {
        "published": True,
        "date__gte": start,
        "date__lte": finish,
    }

    if country:
        filters["country__in"] = country
    if state:
        filters["state__in"] = state
    if county:
        filters["county__in"] = county

    queryset = Checklist.objects.filter(**filters)
    total = queryset.aggregate(Sum("duration"))["duration__sum"] or 0

    if total == 0:
        hours = 0
    elif total < 60:
        hours = "< 1"
    else:
        hours = int(total / 60)

    return {
        "title": _("Hours spent birding"),
        "count": hours,
    }
