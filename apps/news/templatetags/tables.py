from django import template
from django.db.models import Case, Count, F, Q, Sum, When
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta

from data.models import Checklist, Observation, Observer

register = template.Library()


@register.inclusion_tag("news/tables/big-lists.html")
def big_lists_table(country_id, state_id, county_id, start, end, show_country):
    queryset = Checklist.objects.filter(date__gte=start, date__lte=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    related = ["state", "county", "location", "observer"]

    if show_country:
        related.append("country")

    checklists = queryset.select_related(*related).order_by("-species_count")[:10]

    return {
        "title": _("Big Lists"),
        "checklists": sorted(list(checklists), key=lambda checklist: checklist.started),
    }


@register.inclusion_tag("news/tables/checklists-submitted.html")
def checklists_submitted_table(country_id, state_id, county_id, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lte=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
        .annotate(byname=F("observer__byname"))
        .annotate(count=Count("observer"))
        .filter(complete=True)
        .order_by("-count")
    )[:10]

    return {"records": observers}


@register.inclusion_tag("news/tables/checklists-duration.html")
def checklists_duration_table(country_id, state_id, county_id, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lte=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
        .annotate(byname=F("observer__byname"))
        .annotate(total=Sum("duration"))
        .filter(duration__isnull=False)
        .order_by("-total")
    )[:10]

    for observer in observers:
        observer["hours"] = "%0d" % (observer["total"] / 60)
        observer["minutes"] = "%02d" % (observer["total"] % 60)

    return {"records": observers}


@register.inclusion_tag("news/tables/checklists-species.html")
def checklists_species_table(country_id, state_id, county_id, start, end, interval):
    filters = Q(observations__date__gte=start)
    filters &= Q(observations__date__lte=end)
    filters &= Q(
        observations__species__category__in=["species", "sub-species", "domestic"]
    )

    if country_id:
        filters &= Q(observations__country_id=country_id)
    elif state_id:
        filters &= Q(observations__state_id=state_id)
    elif county_id:
        filters &= Q(observations__county_id=county_id)

    observers = (
        Observer.objects.values("name", "byname")
        .annotate(
            count=Count(
                Case(
                    When(
                        filters,
                        then="observations__species",
                    )
                ),
                distinct=True,
            )
        )
        .order_by("-count")[:10]
    )
    return {
        "records": [observer for observer in observers if observer["count"]],
        "interval": interval,
    }


@register.inclusion_tag("news/tables/yearlist.html", takes_context=True)
def yearlist_table(context):
    filters = (
        Q(species__category="species")
        & Q(date__gte=context["start_year"])
        & Q(date__lte=context["end_year"])
    )

    if context.get("country"):
        filters &= Q(country_id=context["country"])
    elif context.get("state"):
        filters &= Q(state_id=context["state"])
    elif context.get("county"):
        filters &= Q(county_id=context["county"])

    year_list = (
        Observation.objects.filter(filters)
        .values_list("id", "species", "date")
        .order_by("species", "started")
        .distinct("species")
    )

    total = len(year_list)

    ids = [
        entry[0]
        for entry in year_list
        if context["start_date"] <= entry[2] <= context["end_date"]
    ]

    related = [
        "checklist",
        "country",
        "state",
        "county",
        "location",
        "species",
        "observer",
    ]

    observations = (
        Observation.objects.filter(id__in=ids)
        .select_related(*related)
        .order_by("species__taxon_order")
    )

    return {
        "title": _("Year List"),
        "start_year": context["start_year"],
        "end_year": context["end_year"],
        "observations": observations,
        "total": total,
        "show_country": context["show_country"],
    }


@register.inclusion_tag("news/tables/big-days.html")
def big_days_table(country_id, state_id, county_id, start, end):
    queryset = (
        Observation.objects.values("observer__identifier", "date")
        .annotate(name=F("observer__name"))
        .annotate(species_count=Count("species", distinct=True))
        .filter(date__gte=start, date__lte=end)
        .filter(species__category="species")
    )

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    entries = queryset.order_by("-species_count")[:10]

    return {
        "title": _("Big Days"),
        "entries": sorted(list(entries), key=lambda entry: entry["date"]),
    }


@register.inclusion_tag("news/tables/high-counts.html", takes_context=True)
def high_counts_table(context):
    filters = Q()

    if context.get("country"):
        filters &= Q(country_id=context["country"])
    elif context.get("state"):
        filters &= Q(state_id=context["state"])
    elif context.get("county"):
        filters &= Q(county_id=context["county"])

    previous = {}
    high_counts = {}

    observations = (
        Observation.objects.filter(filters)
        .filter(
            species__category="species",
            date__gte=context["start_date"] - relativedelta(months=1),
            date__lte=context["end_date"],
            count__gt=0,
        )
        .values_list("id", "species_id", "date")
        .order_by("species__taxon_order", "-count")
    )

    for observation in observations:
        key = observation[1]
        previous.setdefault(key, 0)
        if observation[2] < context["start_date"]:
            previous[key] += 1
        else:
            if previous[key] < 3 and key not in high_counts:
                high_counts[key] = observation[0]

    high_counts = (
        Observation.objects.filter(id__in=high_counts.values())
        .select_related(
            "species", "country", "state", "county", "location", "observer", "checklist"
        )
        .order_by("date", "species__taxon_order")
    )

    return {
        "observations": high_counts,
        "show_country": context["show_country"],
    }
