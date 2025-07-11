from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from filters.forms import (
    CategoryFilter,
    DateRangeFilter,
    FamilyFilter,
    LocationFilter,
    ObserverFilter,
    SpeciesOrder,
)
from ebird.api.data.models import Country, Observation
from filters.views import FilteredListView


class SpeciesView(FilteredListView):
    default_filter = Q(published=True)
    form_classes = (
        LocationFilter,
        ObserverFilter,
        DateRangeFilter,
        CategoryFilter,
        FamilyFilter,
        SpeciesOrder,
    )
    model = Observation
    template_name = "species/list.html"
    url = "species:list"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.extra["location"] = {"show_country": self.show_country}

    def get_url(self):
        return reverse(self.url)

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

    def get_filtered_queryset(self, forms):
        return super().get_filtered_queryset(forms).distinct("species")

    def get_translated_urls(self):
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((self.get_url(), name))
        return urls

    def get_species_column_title(self):
        if category := self.request.GET.get("category"):
            if category == "species":
                title = _("species.singular")
            elif category == "issf":
                title = _("Subspecies")
            elif category == "domestic":
                title = _("Domestics")
            elif category == "hybrid":
                title = _("Hybrids")
            else:
                title = _("Species, Forms, etc.")
        else:
            title = _("Species, Forms, etc.")
        return title

    def get_date_column_title(self):
        if order := self.request.GET.get("order"):
            if order == "species,started":
                title = _("First Seen")
            elif order == "species,-started":
                title = _("Last Seen")
            elif order == "species,-count":
                title = _("Date")
            else:
                title = _("First Seen")
        else:
            title = _("First Seen")
        return title

    def get_count_column_title(self):
        if order := self.request.GET.get("order"):
            if order == "species,-count":
                title = _("Highest Count")
            else:
                title = _("Count")
        else:
            title = _("Count")
        return title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_country"] = self.show_country
        context["translations"] = self.get_translated_urls()
        context["species_column_title"] = self.get_species_column_title()
        context["date_column_title"] = self.get_date_column_title()
        context["count_column_title"] = self.get_count_column_title()
        context["species_list"] = sorted(
            list(context["object_list"]), key=lambda obj: obj.species.taxon_order
        )
        return context
