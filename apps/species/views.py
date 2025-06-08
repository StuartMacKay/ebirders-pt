from django.conf import settings
from django.db.models import OuterRef, Q, Subquery
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import override
from django.views import generic

from django_filters.views import FilterView
from ebird.codes.locations import is_country_code, is_county_code, is_state_code

from data.models import Country, County, Observation, Species, State
from species.filters import SpeciesFilter


class SpeciesView(FilterView):
    model = Observation
    filterset_class = SpeciesFilter
    template_name = "species/list.html"

    def get_queryset(self):
        related = ["checklist", "country", "state", "county", "location", "observer", "species"]
        queryset = super().get_queryset().filter(species__category="species").select_related(*related)
        filtered_queryset = self.filterset_class(self.request.GET, queryset).qs
        return filtered_queryset

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with override(code):
                urls.append((reverse("species:list"), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_country"] = Country.objects.all().count() > 1
        context["translations"] = self.get_translations()
        context["species_list"] = sorted(list(context["object_list"]), key=lambda obj: obj.species.taxon_order)
        return context


class YearlistView(generic.TemplateView):
    template_name = "species/yearlist.html"

    @staticmethod
    def get_translations(year):
        urls = []
        for code, name in settings.LANGUAGES:
            with override(code):
                urls.append((reverse("species:yearlist", kwargs={"year": year}), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = self.kwargs["year"]

        code = self.request.GET.get("code", "")
        filters = Q(date__year=context["year"])
        place = ""

        show_country = Country.objects.all().count() > 1

        if is_country_code(code):
            country = Country.objects.get(code=code)
            filters &= Q(country_id=country.pk)
            place = country.place
        elif is_state_code(code):
            state = State.objects.get(code=code)
            filters &= Q(state_id=state.pk)
            place = state.place
        elif is_county_code(code):
            county = County.objects.get(code=code)
            filters &= Q(county_id=county.pk)
            place = county.place

        if not show_country:
            place = ", ".join(place.split(", ")[:-1])

        observations = (
            Observation.objects.filter(species=OuterRef("pk"))
            .filter(filters)
            .order_by("started")
        )

        # Interestingly, using values_list() to fetch only the 'first'
        # attribute slows the query by a factor of four.
        species = Species.objects.filter(category="species").annotate(
            first=Subquery(observations.values("pk")[:1])
        )

        ids = [obj.first for obj in species]

        observations = (
            Observation.objects.filter(pk__in=ids)
            .select_related(
                "checklist",
                "country",
                "state",
                "county",
                "location",
                "species",
                "observer",
            )
            .order_by("species__taxon_order")
        )

        return {
            "title": _("Year List"),
            "year": str(context["year"]),
            "place": place,
            "observations": observations,
            "total": len(observations),
            "show_country": show_country,
            "translations": self.get_translations(context["year"]),
        }
