from django.conf import settings
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property

from data.models import Country, Observation
from data.views import FilteredListView

from .forms import ObservationFilterForm


class ObservationsView(FilteredListView):
    form_class = ObservationFilterForm
    model = Observation
    template_name = "observations/list.html"
    paginate_by = 100
    url = reverse_lazy("observations:list")

    def get_url(self):
        return self.url

    @cached_property
    def show_country(self):
        return Country.objects.all().count() > 1

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["show_country"] = self.show_country
        return kwargs

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
