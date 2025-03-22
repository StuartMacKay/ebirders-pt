from django import template
from django.db.models import Case, Count, F, Q, Sum, When
from django.utils.translation import gettext_lazy as _

from checklists.models import Checklist, Observer
from ebird.codes.locations import is_country_code, is_state_code, is_county_code

register = template.Library()


@register.inclusion_tag("dashboards/tables/big-lists.html")
def big_lists_table(region, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if is_county_code(region):
        queryset = queryset.filter(location__district__code=region)
    elif is_state_code(region):
        queryset = queryset.filter(location__region__code=region)
    elif is_country_code(region):
        queryset = queryset.filter(location__country__code=region)

    checklists = queryset.order_by(
        "-species_count"
    )[:10]

    return {
        "title": _("Big Lists"),
        "checklists": sorted(list(checklists), key=lambda checklist: checklist.started),
    }


@register.inclusion_tag("dashboards/tables/checklists-submitted.html")
def checklists_submitted_table(region, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if is_county_code(region):
        queryset = queryset.filter(location_district__code=region)
    elif is_state_code(region):
        queryset = queryset.filter(location__region__code=region)
    elif is_country_code(region):
        queryset = queryset.filter(location__country__code=region)

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
        .annotate(count=Count("observer"))
        .filter(complete=True)
        .order_by("-count")
    )[:10]

    return {"observers": observers}


@register.inclusion_tag("dashboards/tables/checklists-duration.html")
def checklists_duration_table(region, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if is_county_code(region):
        queryset = queryset.filter(location__district__code=region)
    elif is_state_code(region):
        queryset = queryset.filter(location__region__code=region)
    elif is_country_code(region):
        queryset = queryset.filter(location__country__code=region)

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
        .annotate(total=Sum("duration"))
        .filter(duration__isnull=False)
        .order_by("-total")
    )[:10]

    for observer in observers:
        observer["hours"] = "%0d" % (observer["total"] / 60)
        observer["minutes"] = "%02d" % (observer["total"] % 60)

    return {"observers": observers}


@register.inclusion_tag("dashboards/tables/checklists-species.html")
def checklists_species_table(region, start, end):
    filters = Q(observations__checklist__date__gte=start)
    filters &= Q(observations__checklist__date__lt=end)
    filters &= (
        Q(observations__species__category="species")
        | Q(observations__species__category="issf"))

    if is_county_code(region):
        filters &= Q(observations__location__district__code=region)
    elif is_state_code(region):
        filters &= Q(observations__location__region__code=region)
    elif is_country_code(region):
        filters &= Q(observations__location__country__code=region)

    observers = Observer.objects.values('name').annotate(
        count=Count(
            Case(
                When(
                    filters,
                    then="observations__species",
                )
            ),
            distinct=True,
        )
    ).order_by("-count")[:10]
    return {"observers": [observer for observer in observers if observer["count"]]}
