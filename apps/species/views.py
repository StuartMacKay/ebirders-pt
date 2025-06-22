from django.conf import settings
from django.urls import reverse_lazy
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from data.forms import (
    CategoryFilter,
    DateRangeFilter,
    LocationFilter,
    ObserverFilter,
    SeenOrder,
)
from data.models import Country, Observation
from data.views import FilteredListView


class SpeciesView(FilteredListView):
    form_classes = (
        LocationFilter,
        ObserverFilter,
        DateRangeFilter,
        CategoryFilter,
        SeenOrder,
    )
    model = Observation
    template_name = "species/list.html"
    url = reverse_lazy("species:list")

    def get_url(self):
        return self.url

    @cached_property
    def show_country(self):
        return Country.objects.all().count() > 1

    def get_related(self):  # noqa
        return [
            "checklist",
            "country",
            "state",
            "county",
            "location",
            "observer",
            "species",
        ]

    def get_queryset(self):
        return super().get_queryset().distinct("species")

    def get_translated_urls(self):
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((self.get_url(), name))
        return urls

    def get_species_list_title(self):
        if category := self.request.GET.get("category"):
            if category == "species":
                title = _("No. of Species")
            elif category == "issf":
                title = _("No. of Subspecies")
            elif category == "domestic":
                title = _("No. of Species")
            elif category == "hybrid":
                title = _("No. of Forms")
            else:
                title = ""
        else:
            title = ""
        return title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_country"] = self.show_country
        context["translations"] = self.get_translated_urls()
        context["species_list_title"] = self.get_species_list_title()
        context["species_list"] = sorted(
            list(context["object_list"]), key=lambda obj: obj.species.taxon_order
        )
        return context
