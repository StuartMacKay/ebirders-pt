from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property

from data.forms import (
    DateRangeFilter,
    LocationFilter,
    ObservationFilter,
    ObservationOrder,
    ObserverFilter,
    SpeciesFilter,
)
from data.models import Country, Observation
from data.views import FilteredListView


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extra["location"] = {"show_country": self.show_country}

    def get_url(self):
        return reverse(self.url)

    @cached_property
    def show_country(self):
        return Country.objects.all().count() > 1

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
        context["show_country"] = self.show_country
        context["translations"] = self.get_translated_urls()
        return context
