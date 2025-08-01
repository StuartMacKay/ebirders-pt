import datetime as dt
import logging

from django import template
from django.db.models import Case, Count, F, Sum, When
from django.utils.translation import gettext_lazy as _

from ebird.api.data.models import Checklist, Observation, Observer

from species.models import CountryList, CountyList, StateList

register = template.Library()
log = logging.getLogger(__name__)


@register.inclusion_tag("news/tables/big-lists.html")
def big_lists(start, finish, country=None, state=None, county=None):
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

    related = ["state", "county", "location", "observer", "country"]

    checklists = (
        Checklist.objects.filter(**filters)
        .select_related(*related)
        .order_by("-species_count", "-date")[:10]
    )

    return {
        "title": _("Big Lists"),
        "checklists": checklists,
    }


@register.inclusion_tag("news/tables/checklists-completed.html")
def checklists_completed(start, finish, country=None, state=None, county=None):
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

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
        .annotate(name=F("observer__name"))
        .annotate(identifier=F("observer__identifier"))
        .annotate(count=Count("observer"))
        .filter(complete=True)
        .order_by("-count")
    )[:10]

    return {
        "records": observers,
    }


@register.inclusion_tag("news/tables/time-spent-birding.html")
def time_spent_birding(start, finish, country=None, state=None, county=None):
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

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
        .annotate(identifier=F("observer__identifier"))
        .annotate(total=Sum("duration"))
        .filter(duration__isnull=False)
        .order_by("-total")
    )[:10]

    for observer in observers:
        observer["hours"] = "%0d" % (observer["total"] / 60)
        observer["minutes"] = "%02d" % (observer["total"] % 60)

    return {
        "records": observers,
    }


@register.inclusion_tag("news/tables/observer-species-latest.html")
def observer_species_latest(start, finish, country=None, state=None, county=None):
    filters = {}

    if country:
        filters["observer_species_latest__country__in"] = country
    if state:
        filters["observer_species_latest__state__in"] = state
    if county:
        filters["observer_species_latest__county__in"] = county

    if filters:
        criteria = Case(When(**filters, then="observer_species_latest__species"))
    else:
        criteria = "observer_species_latest__species"

    records = (
        Observer.objects.values("identifier", "name")
        .annotate(count=Count(criteria, distinct=True))
        .order_by("-count")[:10]
    )

    return {
        "start": start.strftime("%Y-%m-%d"),
        "finish": finish.strftime("%Y-%m-%d"),
        "records": [record for record in records if record["count"]],
    }


@register.inclusion_tag("news/tables/observer-species-weekly.html")
def observer_species_weekly(
    start, finish, week, year, country=None, state=None, county=None
):
    filters = {
        "observer_species_weekly__week": week,
        "observer_species_weekly__year": year,
    }

    if country:
        filters["observer_species_weekly__country__in"] = country
    if state:
        filters["observer_species_weekly__state__in"] = state
    if county:
        filters["observer_species_weekly__county__in"] = county

    records = (
        Observer.objects.values("identifier", "name")
        .annotate(
            count=Count(
                Case(When(**filters, then="observer_species_weekly__species")),
                distinct=True,
            )
        )
        .order_by("-count")[:10]
    )

    return {
        "start": start.strftime("%Y-%m-%d"),
        "finish": finish.strftime("%Y-%m-%d"),
        "records": [record for record in records if record["count"]],
    }


@register.inclusion_tag("news/tables/observer-species-monthly.html")
def observer_species_monthly(
    start, finish, month, year, country=None, state=None, county=None
):
    filters = {
        "observer_species_monthly__month": month,
        "observer_species_monthly__year": year,
    }

    if country:
        filters["observer_species_monthly__country__in"] = country
    if state:
        filters["observer_species_monthly__state__in"] = state
    if county:
        filters["observer_species_monthly__county__in"] = county

    records = (
        Observer.objects.values("identifier", "name")
        .annotate(
            count=Count(
                Case(When(**filters, then="observer_species_monthly__species")),
                distinct=True,
            )
        )
        .order_by("-count")[:10]
    )

    return {
        "start": start.strftime("%Y-%m-%d"),
        "finish": finish.strftime("%Y-%m-%d"),
        "records": [record for record in records if record["count"]],
    }


@register.inclusion_tag("news/tables/year-list.html")
def year_list(start, finish, year, country=None, state=None, county=None):
    filters = {
        "date__gte": dt.date(year=year, month=1, day=1),
        "date__lte": finish,
        "category": "species"
    }

    if county:
        filters["county__in"] = county
        list_class = CountyList
    elif state:
        filters["state__in"] = state
        list_class = StateList
    elif country:
        filters["country__in"] = country
        list_class = CountryList
    else:
        list_class = CountryList

    records = (
        list_class.objects.values_list("identifier", "date")
        .filter(**filters)
        .distinct("species")
        .order_by("species", "started")
    )

    total = records.count()

    ids = [record[0] for record in records if start <= record[1] <= finish]

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
        list_class.objects.filter(identifier__in=ids)
        .select_related(*related)
        .order_by("species__taxon_order")
    )

    return {
        "observations": observations,
        "total": total,
    }


@register.inclusion_tag("news/tables/big-days.html")
def big_days(start, finish, country=None, state=None, county=None):
    filters = {
        "published": True,
        "date__gte": start,
        "date__lte": finish,
        "species__category": "species",
    }

    if country:
        filters["country__in"] = country
    if state:
        filters["state__in"] = state
    if county:
        filters["county__in"] = county

    queryset = (
        Observation.objects.values("observer__identifier", "date")
        .filter(**filters)
        .annotate(name=F("observer__name"))
        .annotate(species_count=Count("species", distinct=True))
    )

    entries = queryset.order_by("-species_count", "-date")[:10]

    return {"title": _("Big Days"), "entries": entries}


@register.inclusion_tag("news/tables/high-counts.html")
def high_counts(start, finish, country=None, state=None, county=None):
    filters = {
        "published": True,
        "date__gte": start,
        "date__lte": finish,
        "species__category": "species",
        "count__gt": 0,
    }

    if country:
        filters["country__in"] = country
    if state:
        filters["state__in"] = state
    if county:
        filters["county__in"] = county

    related = [
        "species",
        "country",
        "state",
        "county",
        "location",
        "observer",
        "checklist",
    ]

    counts = (
        Observation.objects.filter(**filters)
        .filter(**filters)
        .select_related(*related)
        .order_by("species__taxon_order", "-count")
        .distinct("species__taxon_order")
    )

    return {"observations": sorted(counts, key=lambda obj: obj.date, reverse=True)}
