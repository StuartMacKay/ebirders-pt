import logging

from django import template
from django.db.models import Case, Count, F, Q, Sum, When
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta
from ebird.api.data.models import Checklist, Observation, Observer

from news.models import (
    YearList,
)

register = template.Library()
log = logging.getLogger(__name__)


@register.inclusion_tag("news/tables/big-lists.html")
def big_lists(country, state, county, start, end):
    log.info(
        "Generating big_lists: %s %s %s %s %s",
        country,
        state,
        county,
        start,
        end,
    )

    queryset = Checklist.objects.filter(published=True, date__gte=start, date__lte=end)

    if country:
        queryset = queryset.filter(country_id=country.pk)
    elif state:
        queryset = queryset.filter(state_id=state.pk)
    elif county:
        queryset = queryset.filter(county_id=county.pk)

    related = ["state", "county", "location", "observer", "country"]

    checklists = queryset.select_related(*related).order_by("-species_count", "-date")[
        :10
    ]

    return {
        "title": _("Big Lists"),
        "country_code": country.code if country else None,
        "state_code": state.code if state else None,
        "county_code": county.code if county else None,
        "checklists": checklists,
        "start": start,
        "finish": end,
    }


@register.inclusion_tag("news/tables/checklists-completed.html")
def checklists_completed(country_id, state_id, county_id, start, end):
    log.info(
        "Generating checklists_completed: %s %s %s %s %s",
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
        "start": start,
        "finish": end,
    }


@register.inclusion_tag("news/tables/time-spent-birding.html")
def time_spent_birding(country_id, state_id, county_id, start, end):
    log.info(
        "Generating time_spent_birding: %s %s %s %s %s",
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

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
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
        "start": start,
        "finish": end,
    }


@register.inclusion_tag("news/tables/observer-species-latest.html")
def observer_species_latest(country_id, state_id, county_id, start, end):
    log.info(
        "Generating big_week: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    if country_id:
        filters = Q(observer_species_latest__country_id=country_id)
    elif state_id:
        filters = Q(observer_species_latest__state_id=state_id)
    elif county_id:
        filters = Q(observer_species_latest__county_id=county_id)
    else:
        filters = Q()

    if filters:
        criteria = Case(When(filters, then="observer_species_latest__species"))
    else:
        criteria = "observer_species_latest__species"

    records = (
        Observer.objects.values("identifier", "name")
        .annotate(count=Count(criteria, distinct=True))
        .order_by("-count")[:10]
    )

    return {
        "records": [record for record in records if record["count"]],
        "start": start,
        "finish": end,
    }


@register.inclusion_tag("news/tables/observer-species-weekly.html")
def observer_species_weekly(country_id, state_id, county_id, start, end):
    log.info(
        "Generating big_week: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    filters = Q(observer_species_weekly__week=start.isocalendar().week)
    filters &= Q(observer_species_weekly__year=start.year)

    if country_id:
        filters &= Q(observer_species_weekly__country_id=country_id)
    elif state_id:
        filters &= Q(observer_species_weekly__state_id=state_id)
    elif county_id:
        filters &= Q(observer_species_weekly__county_id=county_id)

    records = (
        Observer.objects.values("identifier", "name")
        .annotate(
            count=Count(
                Case(When(filters, then="observer_species_weekly__species")),
                distinct=True,
            )
        )
        .order_by("-count")[:10]
    )

    return {
        "records": [record for record in records if record["count"]],
        "start": start,
        "finish": end,
    }


@register.inclusion_tag("news/tables/observer-species-monthly.html")
def observer_species_monthly(country_id, state_id, county_id, start, end):
    log.info(
        "Generating big_month: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    filters = Q(observer_species_monthly__year=start.year)
    filters &= Q(observer_species_monthly__month=start.month)

    if country_id:
        filters &= Q(observer_species_monthly__country_id=country_id)
    elif state_id:
        filters &= Q(observer_species_monthly__state_id=state_id)
    elif county_id:
        filters &= Q(observer_species_monthly__county_id=county_id)

    records = (
        Observer.objects.values("identifier", "name")
        .annotate(
            count=Count(
                Case(When(filters, then="observer_species_monthly__species")),
                distinct=True,
            )
        )
        .order_by("-count")[:10]
    )

    return {
        "records": [record for record in records if record["count"]],
        "start": start,
        "finish": end,
    }


@register.inclusion_tag("news/tables/year-list.html")
def year_list(country_id, state_id, county_id, start, end):
    log.info(
        "Generating yearlist: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    start_year = start.replace(month=1, day=1)
    end_year = end.replace(month=12, day=31)

    filters = Q(date__gte=start_year) & Q(date__lte=end_year)

    if country_id:
        filters &= Q(country_id=country_id)
    elif state_id:
        filters &= Q(state_id=state_id)
    elif county_id:
        filters &= Q(county_id=county_id)

    records = (
        YearList.objects.values_list("identifier", "date")
        .filter(filters)
        .distinct("species")
        .order_by("species", "date")
    )

    total = records.count()

    ids = [record[0] for record in records if start <= record[1] <= end]

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
        YearList.objects.filter(identifier__in=ids)
        .select_related(*related)
        .order_by("species__taxon_order")
    )

    return {
        "country": country_id,
        "state": state_id,
        "county": county_id,
        "start_year": start_year,
        "end_year": end_year,
        "observations": observations,
        "total": total,
    }


@register.inclusion_tag("news/tables/big-days.html")
def big_days(country_id, state_id, county_id, start, end):
    log.info(
        "Generating big_days: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    queryset = (
        Observation.objects.values("observer__identifier", "date")
        .annotate(name=F("observer__name"))
        .annotate(species_count=Count("species", distinct=True))
        .filter(published=True)
        .filter(date__gte=start, date__lte=end)
        .filter(species__category="species")
    )

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif state_id:
        queryset = queryset.filter(state_id=state_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    entries = queryset.order_by("-species_count", "-date")[:10]

    return {"title": _("Big Days"), "entries": entries}


@register.inclusion_tag("news/tables/high-counts.html")
def high_counts(country_id, state_id, county_id, start, end):
    log.info(
        "Generating high_counts: %s %s %s %s %s",
        country_id,
        state_id,
        county_id,
        start,
        end,
    )

    filters = Q(published=True)

    if country_id:
        filters &= Q(country_id=country_id)
    elif state_id:
        filters &= Q(state_id=state_id)
    elif county_id:
        filters &= Q(county_id=county_id)

    previous = {}
    high_counts = {}

    observations = (
        Observation.objects.filter(filters)
        .filter(
            species__category="species",
            date__gte=start - relativedelta(months=1),
            date__lte=end,
            count__gt=0,
        )
        .values_list("identifier", "species_id", "date")
        .order_by("species__taxon_order", "-count")
    )

    for observation in observations:
        key = observation[1]
        previous.setdefault(key, 0)
        if observation[2] < start:
            previous[key] += 1
        else:
            if previous[key] < 3 and key not in high_counts:
                high_counts[key] = observation[0]

    high_counts = (
        Observation.objects.filter(identifier__in=high_counts.values())
        .select_related(
            "species", "country", "state", "county", "location", "observer", "checklist"
        )
        .order_by("-date", "species__taxon_order")
    )

    return {
        "observations": high_counts,
    }
