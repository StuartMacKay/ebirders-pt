import re

from django.http import JsonResponse
from django.views import generic

from ebird.codes.locations import is_country_code, is_subnational1_code, \
    is_subnational2_code, is_location_code

from checklists.models import Checklist, Country, County, District, Observer


class ChecklistsView(generic.ListView):
    model = Checklist
    template_name = "checklists/index.html"
    paginate_by = 50
    ordering = ("-started",)

    def get_filters(self):
        filters = {
            "country": self.request.GET.get("country"),
            "district": self.request.GET.get("district"),
            "county": self.request.GET.get("county"),
            "location": self.request.GET.get("location"),
            "observer": self.request.GET.get("observer"),
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
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = self.get_filters()
        context["search"] = self.request.GET.get("search", "")
        context["show_country"] = Country.objects.all().count() > 1
        return context


class DetailView(generic.DetailView):
    model = Checklist
    template_name = "checklists/detail.html"
    context_object_name = "checklist"

    def get_object(self, queryset=None):
        return Checklist.objects.get(identifier=self.kwargs["identifier"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["observations"] = context["checklist"].observations.all()
        return context


def autocomplete(request):
    """
    Return the list of countries, regions and districts for the search
    field. If there is only one country, remove it from the label.
    """
    data = []

    for code, place in Country.objects.all().values_list("code", "place"):
        data.append(
            {
                "value": code,
                "label": place,
            }
        )

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

    for code, name in Observer.objects.all().values_list("pk", "name"):
        data.append({"value": code, "label": name})

    return JsonResponse(data, safe=False)
