from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.utils import translation

from ebird.api.data.models import Observation

from filters.forms import (
    DateRangeFilter,
    LocationFilter,
    ObservationFilter,
    ObservationOrder,
    ObserverFilter,
    SpeciesFilter,
)
from filters.views import FilteredListView


class ObservationsView(FilteredListView):
    default_filter = Q(published=True)
    form_classes = (
        LocationFilter,
        ObserverFilter,
        DateRangeFilter,
        SpeciesFilter,
        ObservationFilter,
        ObservationOrder,
    )
    model = Observation
    template_name = "observations/list.html"
    paginate_by = 100
    url = "observations:list"

    def get_url(self):
        return reverse(self.url)

    def get_related(self):  # noqa
        return ["country", "state", "county", "location", "observer", "species"]

    def get_translated_urls(self):
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((self.get_url(), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["translations"] = self.get_translated_urls()
        return context
