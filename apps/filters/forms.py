import json

from django import forms
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from dal import autocomplete
from ebird.api.data.models import Country, County, Location, Observer, Species, State


class FilterForm(forms.Form):
    form_id = None
    form_title = None
    filters = {}

    def get_filters(self):
        return {
            expr: self.cleaned_data[field]
            for field, expr in self.filters.items()
            if self.cleaned_data.get(field)
        }

    def get_ordering(self):
        return []


class LocationFilter(FilterForm):
    form_id = "location"
    form_title = _("By Location")

    country = forms.ModelChoiceField(
        label=_("Country"),
        required=False,
        queryset=Country.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="filters:countries",
            attrs={"placeholder": _("Select one or more countries")},
        ),
    )

    state = forms.ModelMultipleChoiceField(
        label=_("Statge"),
        required=False,
        queryset=State.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="filters:states",
            forward=["country"],
            attrs={
                "data-placeholder": _("Select one or more states"),
            },
        ),
    )

    county = forms.ModelMultipleChoiceField(
        label=_("County"),
        required=False,
        queryset=County.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="filters:counties",
            forward=["state", "country"],
            attrs={
                "data-placeholder": _("Select one or more counties"),
            },
        ),
    )

    location = forms.ModelMultipleChoiceField(
        label=_("Location"),
        required=False,
        queryset=Location.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="filters:locations",
            forward=["county", "state", "country"],
            attrs={
                "data-placeholder": _("Select one or more locations"),
            },
        ),
    )

    hotspot = forms.ChoiceField(
        label=_("Hotspots only"),
        choices=(
            ("", _("No")),
            ("True", _("Yes")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    filters = {
        "country": "country__in",
        "state": "state__in",
        "county": "county__in",
        "location": "location__in",
        "hotspot": "location__hotspot",
    }


class ObserverFilter(FilterForm):
    form_id = "observer"
    form_title = _("By Observer")

    observer = forms.ModelChoiceField(
        label=_("Observer"),
        required=False,
        queryset=Observer.objects.all(),
        widget=autocomplete.Select2(
            url="filters:observers",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    filters = {
        "observer": "observer",
    }


class SpeciesFilter(FilterForm):
    form_id = "species"
    form_title = _("By Species")

    common_name = forms.ModelChoiceField(
        label=_("Common name"),
        required=False,
        queryset=Species.objects.all(),
        widget=autocomplete.Select2(
            url="filters:common-name",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    scientific_name = forms.ModelChoiceField(
        label=_("Scientific name"),
        required=False,
        queryset=Species.objects.all(),
        widget=autocomplete.Select2(
            url="filters:scientific-name",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    family = forms.ChoiceField(
        label=_("Family"),
        required=False,
        widget=autocomplete.Select2(
            url="filters:families",
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
            url="filters:families",
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


class DateRangeFilter(FilterForm):
    form_id = "date-range"
    form_title = _("By Date")

    DATES_SWAPPED = _("This date is later than the until date.")

    start = forms.DateField(
        label=_("From"),
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    finish = forms.DateField(
        label=_("Until"),
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    filters = {
        "start": "date__gte",
        "finish": "date__lte",
    }

    def clean(self):
        start = self.cleaned_data.get("start")
        finish = self.cleaned_data.get("finish")

        if start and finish and start > finish:
            self.add_error("start", self.DATES_SWAPPED)


class ProtocolFilter(FilterForm):
    form_id = "protocol"
    form_title = _("By Protocol")

    protocol = forms.ChoiceField(
        label=_("Protocol"),
        choices=(
            ("P22", _("Travelling")),
            ("P21", _("Stationary")),
            ("P62", _("Historical")),
            ("P20", _("Incidental")),
            ("P23", _("Area")),
            ("P33", _("Banding")),
            ("P60", _("Pelagic")),
            ("P54", _("Nocturnal Flight Call Count")),
            ("P48", _("Random")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    complete = forms.ChoiceField(
        label=_("Status"),
        choices=(
            ("", _("All")),
            ("True", _("Complete")),
            ("False", _("Incomplete")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    filters = {
        "protocol": "protocol_code",
        "complete": "complete"
    }


class ObservationFilter(FilterForm):
    form_id = "observation"
    form_title = _("Options")

    approved = forms.ChoiceField(
        label=_("Status"),
        choices=(
            ("", _("All")),
            ("True", _("Accepted")),
            ("False", _("Rejected")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    audio = forms.ChoiceField(
        label=_("With audio"),
        choices=(
            ("", _("All")),
            ("True", _("Yes")),
            ("False", _("No")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    photo = forms.ChoiceField(
        label=_("With photos"),
        choices=(
            ("", _("All")),
            ("True", _("Yes")),
            ("False", _("No")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    video = forms.ChoiceField(
        label=_("With video"),
        choices=(
            ("", _("All")),
            ("True", _("Yes")),
            ("False", _("No")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    filters = {
        "approved": "approved",
        "audio": "audio",
        "photo": "photo",
        "video": "video"
    }


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


class ChecklistOrder(FilterForm):
    form_id = "checklist-order"
    form_title = _("Order By")

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("-started", _("Most recent first")),
            ("-species_count,-started", _("Number of species")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return order.split(",")
        return ("-started",)


class ObservationOrder(FilterForm):
    form_id = "observation-order"
    form_title = _("Order By")

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("-started", _("Most recent first")),
            ("-count", _("Highest count first")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return (order,)
        return ("-started",)


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
