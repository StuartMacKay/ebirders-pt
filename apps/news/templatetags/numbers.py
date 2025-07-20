import logging

from django import template
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from ebird.api.data.models import Checklist, Observation

register = template.Library()
log = logging.getLogger(__name__)


@register.inclusion_tag("news/numbers/number.html")
def species_count(country_id, state_id, county_id, start, end):
    log.info(
        "Generating species_count: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    queryset = Observation.objects.filter(date__gte=start, date__lte=end).filter(
        species__category="species"
    )

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    count = queryset.values_list("species_id", flat=True).distinct().count()

    return {
        "title": _("species.plural"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def checklist_count(country_id, state_id, county_id, start, end):
    log.info(
        "Generating checklist_count: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )
    queryset = Checklist.objects.filter(published=True, date__gte=start, date__lte=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    count = queryset.count()

    return {
        "title": _("Checklists"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def observer_count(country_id, state_id, county_id, start, end):
    log.info(
        "Generating observer_count: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    queryset = Checklist.objects.filter(published=True, date__gte=start, date__lte=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    count = queryset.values_list("observer_id", flat=True).distinct().count()

    return {
        "title": _("Observers"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def duration_count(country_id, state_id, county_id, start, end):
    log.info(
        "Generating duration_count: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    queryset = Checklist.objects.filter(published=True, date__gte=start, date__lte=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    total = queryset.aggregate(Sum("duration"))["duration__sum"] or 0

    if total == 0:
        hours = 0
    elif total < 60:
        hours = "< 1"
    else:
        hours = int(total / 60)

    return {
        "title": _("Hours birding"),
        "count": hours,
    }
