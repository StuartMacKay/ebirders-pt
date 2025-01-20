from dal import autocomplete
from django_filters.views import FilterView
from ebird.checklists.models import Checklist

from .filters import ChecklistFilter
from .queries import country_choices, state_choices, county_choices


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
        state = self.forwarded.get("state")
        return county_choices(state)


class ChecklistsView(FilterView):
    model = Checklist
    filterset_class = ChecklistFilter
    template_name = "checklists/index.html"
    paginate_by = 50
    ordering = ("-date", "-time")

    def get_queryset(self):
        return self.filterset_class(
            self.request.GET,
            queryset=super().get_queryset().select_related("location", "observer"),
        ).qs
