import json

from django.conf import settings
from django.db.models import Q
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from dal import autocomplete
from ebird.api.data.models import Observation, Species

from base.views import FilteredListView
from dates.forms import DateRangeFilter
from locations.forms import LocationFilter
from observers.forms import ObserverFilter

from .forms import CategoryFilter, FamilyFilter, SpeciesOrder


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

    def get_url(self):
        return reverse(self.url)

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
        context["translations"] = self.get_translated_urls()
        context["species_column_title"] = self.get_species_column_title()
        context["date_column_title"] = self.get_date_column_title()
        context["count_column_title"] = self.get_count_column_title()
        context["species_list"] = sorted(
            list(context["object_list"]), key=lambda obj: obj.species.taxon_order
        )
        return context


class CommonNameList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = (
            Species.objects.all()
            .values_list("species_code", "common_name")
            .order_by("taxon_order")
        )
        return [
            ("%s" % code, json.loads(name)[self.request.LANGUAGE_CODE])
            for code, name in queryset
        ]


class ScientificNameList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = (
            Species.objects.all()
            .values_list("species_code", "scientific_name")
            .order_by("taxon_order")
        )
        return [(code, name) for code, name in queryset]


class FamilyList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = (
            Species.objects.all()
            .values_list("family_code", "family_scientific_name")
            .order_by("taxon_order")
        )
        return list({(code, name) for code, name in queryset})
