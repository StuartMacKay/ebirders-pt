from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.utils import translation

from ebird.api.data.models import Checklist

from base.views import FilteredListView
from dates.forms import DateRangeFilter
from locations.forms import LocationFilter
from observers.forms import ObserverFilter

from .forms import ChecklistOrder, ProtocolFilter


class ChecklistsView(FilteredListView):
    default_filter = Q(published=True)
    form_classes = [
        LocationFilter,
        ObserverFilter,
        DateRangeFilter,
        ProtocolFilter,
        ChecklistOrder,
    ]
    model = Checklist
    paginate_by = 50
    template_name = "checklists/list.html"
    url = "checklists:list"

    def get_url(self):
        return reverse(self.url)

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
        context["translations"] = self.get_translated_urls()
        return context
