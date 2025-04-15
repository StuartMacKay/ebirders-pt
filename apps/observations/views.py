import re

from django.http import JsonResponse
from django.utils.translation import get_language
from django.views import generic
from ebird.codes.locations import (
    is_country_code,
    is_subnational1_code,
    is_subnational2_code,
    is_location_code,
)

from data.models import Observation, Country, District, County, Species, Observer


class ObservationsView(generic.ListView):
    model = Observation
    template_name = "observations/index.html"
    paginate_by = 50
    ordering = ("-started",)

    def get_filters(self):
        filters = {
            "country": self.request.GET.get("country"),
            "district": self.request.GET.get("district"),
            "county": self.request.GET.get("county"),
            "location": self.request.GET.get("location"),
            "observer": self.request.GET.get("observer"),
            "species": self.request.GET.get("species"),
        }

        if code := self.request.GET.get("code"):
            if is_country_code(code):
                filters["country"] = code
            elif is_subnational1_code(code):
                filters["district"] = code
            elif is_subnational2_code(code):
                filters["county"] = code
            elif is_location_code(code):
                filters["location"] = code
            elif 4 < len(code) < 8:
                filters["species"] = code
            else:
                filters["observer"] = code

        return filters

    def get_queryset(self):
        qs = super().get_queryset()
        filters = self.get_filters()

        if country := filters.get("country"):
            qs = qs.filter(country__code=country)
        elif district := filters.get("district"):
            qs = qs.filter(district__code=district)
        elif county := filters.get("county"):
            qs = qs.filter(county__code=county)
        elif location := filters.get("location"):
            qs = qs.filter(location__identifier=location)
        elif species := filters.get("species"):
            qs = qs.filter(species__species_code=species)
        elif observer := filters.get("observer"):
            qs = qs.filter(observer__pk=observer)

        return qs.select_related(
            "country",
            "region",
            "district",
            "county",
            "area",
            "location",
            "observer",
            "species",
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = self.get_filters()
        context["search"] = self.request.GET.get("search", "")
        context["show_country"] = Country.objects.all().count() > 1
        return context


def autocomplete(request):
    """
    Return the list of countries, regions and districts for the search
    field. If there is only one country, remove it from the label.
    """
    language = get_language()

    data = []

    for code, place in Country.objects.all().values_list("code", "place"):
        data.append({"value": code, "label": place})

    if len(data) == 1:
        country = data.pop(0)["label"]
    else:
        country = None

    for code, place in District.objects.all().values_list("code", "place"):
        if country:
            label = re.sub(r", %s$" % country, "", place)
        else:
            label = place
        data.append({"value": code, "label": label})

    for code, place in County.objects.all().values_list("code", "place"):
        if country:
            label = re.sub(r", %s$" % country, "", place)
        else:
            label = place
        data.append({"value": code, "label": label})

    for code, common_name, translations in Species.objects.all().values_list(
        "species_code", "common_name", "data"
    ):
        if language in translations["common_name"]:
            name = translations["common_name"][language]
        else:
            name = common_name
        data.append({"value": code, "label": name})

    for code, name in Species.objects.all().values_list(
        "species_code", "scientific_name"
    ):
        data.append({"value": code, "label": name})

    for code, name in Observer.objects.all().values_list("pk", "name"):
        data.append({"value": code, "label": name})

    return JsonResponse(data, safe=False)
