from django import template
from django.db.models import Case, Count, F, Min, Q, Sum, When
from django.utils.translation import gettext_lazy as _

from data.models import Checklist, Observer, Observation, Species

register = template.Library()


@register.inclusion_tag("news/tables/big-lists.html")
def big_lists_table(country_id, district_id, county_id, start, end, show_country):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif district_id:
        queryset = queryset.filter(district_id=district_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    related = ["district", "county", "location", "observer"]

    if show_country:
        related.append("country")

    checklists = queryset.select_related(*related).order_by("-species_count")[:10]

    return {
        "title": _("Big Lists"),
        "checklists": sorted(list(checklists), key=lambda checklist: checklist.started),
    }


@register.inclusion_tag("news/tables/checklists-submitted.html")
def checklists_submitted_table(country_id, district_id, county_id, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif district_id:
        queryset = queryset.filter(district_id=district_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

    observers = (
        queryset.values("observer")
        .annotate(name=F("observer__name"))
        .annotate(count=Count("observer"))
        .filter(complete=True)
        .order_by("-count")
    )[:10]

    return {"observers": observers}


@register.inclusion_tag("news/tables/checklists-duration.html")
def checklists_duration_table(country_id, district_id, county_id, start, end):
    queryset = Checklist.objects.filter(date__gte=start, date__lt=end)

    if country_id:
        queryset = queryset.filter(country_id=country_id)
    elif district_id:
        queryset = queryset.filter(district_id=district_id)
    elif county_id:
        queryset = queryset.filter(county_id=county_id)

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


@register.inclusion_tag("news/tables/checklists-species.html")
def checklists_species_table(country_id, district_id, county_id, start, end):
    filters = Q(observations__date__gte=start)
    filters &= Q(observations__date__lt=end)
    filters &= Q(observations__identified=True)

    if country_id:
        filters &= Q(observations__country_id=country_id)
    elif district_id:
        filters &= Q(observations__district_id=district_id)
    elif county_id:
        filters &= Q(observations__county_id=county_id)

    observers = (
        Observer.objects.values("name")
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
    return {"observers": [observer for observer in observers if observer["count"]]}


@register.inclusion_tag("news/tables/yearlist.html", takes_context=True)
def yearlist_table(context):
    filters = Q()

    if context["country"]:
        filters &= Q(observations__country_id=context["country"])
    elif context["district"]:
        filters &= Q(observations__district_id=context["district"])
    elif context["county"]:
        filters &= Q(observations__county_id=context["county"])

    species = Species.objects.filter(category="species")

    if filters:
        species = species.annotate(
            added=Min(Case(When(filters, then="observations__date")))
        )
    else:
        species = species.annotate(added=Min("observations__date"))

    species = species.filter(added__gte=context["week_start"], added__lt=context["week_end"]).order_by("added")

    observations = []

    filters = Q()

    if context["country"]:
        filters &= Q(country_id=context["country"])
    elif context["district"]:
        filters &= Q(district_id=context["district"])
    elif context["county"]:
        filters &= Q(county_id=context["county"])

    for item in species:
        observations.append(
            Observation.objects.filter(date=item.added, species_id=item.pk)
            .filter(filters)
            .select_related(
                "checklist",
                "country",
                "district",
                "county",
                "location",
                "species",
                "observer",
            )
            .first()
        )


    total = (
        Observation.objects
        .filter(filters)
        .filter(species__category="species")
        .filter(date__lt=context["week_end"], date__year=context["year"])
        .distinct()
        .values('species_id')
        .count()
    )

    return {
        "title": _("Year List"),
        "year": str(context["year"]),
        "observations": observations,
        "total": total,
        "show_country": context["show_country"],
    }
