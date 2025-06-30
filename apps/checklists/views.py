from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property

from data.forms import (
    ChecklistOrder,
    DateRangeFilter,
    LocationFilter,
    ObserverFilter,
)
from data.models import Checklist, Country
from data.views import FilteredListView


class ChecklistsView(FilteredListView):
    form_classes = (
        LocationFilter,
        ObserverFilter,
        DateRangeFilter,
        ChecklistOrder,
    )
    model = Checklist
    paginate_by = 50
    template_name = "checklists/list.html"
    url = "checklists:list"

    def get_url(self):
        return reverse(self.url)

    @cached_property
    def show_country(self):
        return Country.objects.all().count() > 1

    def get_related(self):  # noqa
        return ["country", "state", "county", "location", "observer"]

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
