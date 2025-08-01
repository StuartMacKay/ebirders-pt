import json

from django import forms
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from dal import autocomplete
from ebird.api.data.models import Species

from base.forms import FilterForm


class CategoryFilter(FilterForm):
    form_id = "category"
    form_title = _("For Category")

    category = forms.ChoiceField(
        label=_("Category"),
        choices=[("", _("All"))] + Species.Category.choices,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    filters = {
        "category": "species__category",
    }


class SpeciesFilter(FilterForm):
    form_id = "species"
    form_title = _("By Species")

    common_name = forms.ModelChoiceField(
        label=_("Common name"),
        required=False,
        queryset=Species.objects.all(),
        widget=autocomplete.Select2(
            url="species:common-names",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    scientific_name = forms.ModelChoiceField(
        label=_("Scientific name"),
        required=False,
        queryset=Species.objects.all(),
        widget=autocomplete.Select2(
            url="species:scientific-names",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    filters = {
        "common_name": "species",
        "scientific_name": "species",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            self.fields["common_name"].choices = self.get_common_name_choice()

    def get_common_name_choice(self):
        choices = []
        if code := self.data.get("common_name"):
            choice = (
                Species.objects.filter(species_code=code)
                .values_list("species_code", "common_name")
                .first()
            )
            if choice:
                choices = [(choice[0], json.loads(choice[1])[get_language()])]
        return choices
