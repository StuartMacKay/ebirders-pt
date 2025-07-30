import json

from django import forms
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from dal import autocomplete
from ebird.api.data.models import Species

from base.forms import FilterForm


class CategoryFilter(FilterForm):
    form_id = "category"
    form_title = _("By Category")

    category = forms.ChoiceField(
        label=_("Category"),
        choices=Species.Category.choices,
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

    family = forms.ChoiceField(
        label=_("Family"),
        required=False,
        widget=autocomplete.Select2(
            url="species:families",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    filters = {
        "common_name": "species",
        "scientific_name": "species",
        "family": "species__family_code",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            self.fields["common_name"].choices = self.get_common_name_choice()
            self.fields["family"].choices = self.get_family_choice()

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

    def get_family_choice(self):
        choices = []
        if code := self.data.get("family"):
            choice = (
                Species.objects.filter(family_code=code)
                .values_list("family_code", "family_scientific_name")
                .first()
            )
            if choice:
                choices = [choice]
        return choices


class FamilyFilter(FilterForm):
    form_id = "family"
    form_title = _("By Family")

    family = forms.ChoiceField(
        label=_("Family"),
        required=False,
        widget=autocomplete.Select2(
            url="species:families",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    filters = {
        "family": "species__family_code",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            self.fields["family"].choices = self.get_family_choice()

    def get_family_choice(self):
        choices = []
        if code := self.data.get("family"):
            choice = (
                Species.objects.filter(family_code=code)
                .values_list("family_code", "family_scientific_name")
                .first()
            )
            if choice:
                choices = [choice]
        return choices


class SpeciesOrder(FilterForm):
    form_id = "species-order"
    form_title = _("Order By")

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("species,started", _("First Seen")),
            ("species,-started", _("Last Seen")),
            ("species,-count", _("Highest Count")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return order.split(",")
        return "species", "started"
