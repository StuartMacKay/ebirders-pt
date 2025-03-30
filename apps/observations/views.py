from dal import autocomplete
from django_filters.views import FilterView

from checklists.models import Observation
from .filters import ObservationFilter
from .queries import (
    country_choices,
    state_choices,
    county_choices,
    location_choices,
    observer_choices,
    species_choices,
)


class Select2TuplesListView(autocomplete.Select2ListView):
    def autocomplete_results(self, results):
        filtered_results = []
        for current_tuple in results:
            name = current_tuple[1]
            print(name.lower())
            if self.q.lower() in name.lower():
                filtered_results.append(current_tuple)

        return filtered_results

    def results(self, results):
        return [dict(id=x[0], text=x[1]) for x in results]


class CountryAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return country_choices()


class StateAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        country = self.forwarded.get("country")
        return state_choices(country)


class CountyAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        country = self.forwarded.get("country")
        state = self.forwarded.get("state")
        return county_choices(country, state)


class LocationAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        country = self.forwarded.get("country")
        state = self.forwarded.get("state")
        county = self.forwarded.get("county")
        return location_choices(country, state, county)


class ObserverAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return observer_choices()


class SpeciesAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return species_choices()


class ObservationsView(FilterView):
    model = Observation
    filterset_class = ObservationFilter
    template_name = "observations/index.html"
    paginate_by = 50
    ordering = ("-checklist__started",)

    def get_queryset(self):
        return self.filterset_class(
            self.request.GET,
            queryset=super()
            .get_queryset()
            .select_related(
                "checklist",
                "country",
                "region",
                "district",
                "location",
                "observer",
                "species",
            ),
        ).qs
