from django import template
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from ebird.codes.locations import is_country_code, is_state_code, is_county_code

from checklists.models import Checklist, Observation

register = template.Library()


@register.inclusion_tag("dashboards/numbers/number.html")
def species_count(region, start, end):
    queryset = Observation.objects.filter(date__gte=start, date__lt=end)

    if is_county_code(region):
        queryset = queryset.filter(district__code=region)
    elif is_state_code(region):
        queryset = queryset.filter(region__code=region)
    elif is_country_code(region):
        queryset = queryset.filter(country__code=region)

    count = (
        queryset
        .values_list("species_id", flat=True)
        .distinct()
        .count()
    )

    return {
        "title": _("Species (plural)"),
        "count": count,
    }


@register.inclusion_tag("dashboards/numbers/number.html")
def checklist_count(region, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if is_county_code(region):
        queryset = queryset.filter(district__code=region)
    elif is_state_code(region):
        queryset = queryset.filter(region__code=region)
    elif is_country_code(region):
        queryset = queryset.filter(country__code=region)

    count = queryset.count()

    return {
        "title": _("Checklists"),
        "count": count,
    }


@register.inclusion_tag("dashboards/numbers/number.html")
def observer_count(region, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if is_county_code(region):
        queryset = queryset.filter(district__code=region)
    elif is_state_code(region):
        queryset = queryset.filter(region__code=region)
    elif is_country_code(region):
        queryset = queryset.filter(country__code=region)

    count = (
        queryset
        .values_list("observer_id", flat=True)
        .distinct()
        .count()
    )

    return {
        "title": _("Observers"),
        "count": count,
    }


@register.inclusion_tag("dashboards/numbers/number.html")
def duration_count(region, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if is_county_code(region):
        queryset = queryset.filter(district__code=region)
    elif is_state_code(region):
        queryset = queryset.filter(region__code=region)
    elif is_country_code(region):
        queryset = queryset.filter(country__code=region)

    total = queryset.aggregate(Sum("duration"))[
        "duration__sum"
    ] or 0

    return {
        "title": _("Hours"),
        "count": int(total / 60),
    }
