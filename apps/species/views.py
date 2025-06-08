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
