from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property
from django.views import generic

from data.forms import (
    ChecklistOrder,
    DateRangeFilter,
    HotspotFilter,
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
        HotspotFilter,
        ChecklistOrder,
    )
    model = Checklist
    paginate_by = 50
    template_name = "checklists/list.html"
    url = reverse_lazy("checklists:list")

    def get_url(self):
        return self.url

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


class DetailView(generic.DetailView):
    model = Checklist
    template_name = "checklists/detail.html"
    context_object_name = "checklist"

    def get_object(self, queryset=None):
        return get_object_or_404(Checklist, identifier=self.kwargs["identifier"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["observations"] = context["checklist"].observations.all()
        return context
