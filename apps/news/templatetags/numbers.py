from django import template
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

from checklists.models import Checklist, Observation

register = template.Library()


@register.inclusion_tag("news/numbers/number.html")
def species_count(country_id, district_id, county_id, start, end):
    queryset = Observation.objects.filter(date__gte=start, date__lt=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif district_id:
        queryset = queryset.filter(district_id=district_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    count = queryset.values_list("species_id", flat=True).distinct().count()

    return {
        "title": _("Species (plural)"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def checklist_count(country_id, district_id, county_id, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif district_id:
        queryset = queryset.filter(district_id=district_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    count = queryset.count()

    return {
        "title": _("Checklists"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def observer_count(country_id, district_id, county_id, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif district_id:
        queryset = queryset.filter(district_id=district_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    count = queryset.values_list("observer_id", flat=True).distinct().count()

    return {
        "title": _("Observers"),
        "count": count,
    }


@register.inclusion_tag("news/numbers/number.html")
def duration_count(country_id, region_id, district_id, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif region_id:
        queryset = queryset.filter(region_id=region_id)
    elif district_id:
        queryset = queryset.filter(district_id=district_id)

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
