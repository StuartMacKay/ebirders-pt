import json

from django import forms
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from data.models import Country, County, Location, Observer, Species, State


class FilterForm(forms.Form):
    identifier = None
    title = None

    def get_filters(self):
        return Q()

    def get_ordering(self):
        return []


class LocationFilter(FilterForm):
    title = _("By Location")
    identifier = "location"

    country = forms.ChoiceField(
        label=_("Country"),
        required=False,
        widget=autocomplete.Select2(
            url="data:countries",
            attrs={
                "placeholder": _("Select one or more countries")
            },
        ),
    )
    state = forms.MultipleChoiceField(
        label=_("State"),
        required=False,
        widget=autocomplete.Select2Multiple(
            url="data:states",
            forward=["country"],
            attrs={
                "data-placeholder": _("Select one or more states"),
            },
        ),
    )

    county = forms.MultipleChoiceField(
        label=_("County"),
        required=False,
        widget=autocomplete.Select2Multiple(
            url="data:counties",
            forward=["state", "country"],
            attrs={
                "data-placeholder": _("Select one or more counties"),
            },
        ),
    )

    location = forms.MultipleChoiceField(
        label=_("Location"),
        required=False,
        widget=autocomplete.Select2Multiple(
            url="data:locations",
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

    def __init__(self, *args, **kwargs):
        show_country = kwargs.pop("show_country")
        super().__init__(*args, **kwargs)

        if not show_country:
            self.fields["country"].widget = forms.HiddenInput()

        if self.is_bound:
            self.fields["country"].choices = self.get_country_choice()
            self.fields["state"].choices = self.get_state_choices()
            self.fields["county"].choices = self.get_county_choices()
            self.fields["location"].choices = self.get_location_choices()

    def get_country_choice(self):
        choices = []
        if country := self.data.get("country"):
            choices = Country.objects.filter(code=country).values_list("code", "name")
        return choices

    def get_state_choices(self):
        choices = []
        if states := self.data.getlist("state"):
            choices = State.objects.filter(code__in=states).values_list("code", "name")
        return choices

    def get_county_choices(self):
        choices = []
        if counties := self.data.getlist("county"):
            choices = County.objects.filter(code__in=counties).values_list(
                "code", "name"
            )
        return choices

    def get_location_choices(self):
        choices = []
        if locations := self.data.getlist("location"):
            choices = (
                Location.objects.all()
                .filter(identifier__in=locations)
                .values_list("identifier", "byname")
            )
        return choices

    def get_filters(self):
        filters = super().get_filters()
        if location := self.cleaned_data.get("location"):
            filters &= Q(location__identifier__in=location)
        elif county := self.cleaned_data.get("county"):
            filters &= Q(county__code__in=county)
        elif states := self.cleaned_data.get("state"):
            filters &= Q(state__code__in=states)
        elif country := self.cleaned_data.get("country"):
            filters &= Q(country__code=country)
        if hotspot := self.cleaned_data.get("hotspot"):
            filters &= Q(location__hotspot=hotspot)
        return filters


class ObserverFilter(FilterForm):
    title = _("By Observer")
    identifier = "observer"

    observer = forms.ChoiceField(
        label=_("Observer"),
        required=False,
        widget=autocomplete.Select2(
            url="data:observers",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            self.fields["observer"].choices = self.get_observer_choice()

    def get_observer_choice(self):
        choices = []
        if observer := self.data.get("observer"):
            choices = Observer.objects.filter(identifier=observer).values_list("identifier", "name")
        return choices

    def get_filters(self):
        filters = super().get_filters()
        if observer := self.cleaned_data.get("observer"):
            filters &= Q(observer__identifier=observer)
        return filters


class SpeciesFilter(FilterForm):
    title = _("By Species")
    identifier = "species"

    species = forms.ChoiceField(
        label=_("Species"),
        required=False,
        widget=autocomplete.Select2(
            url="data:species",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            self.fields["species"].choices = self.get_species_choice()

    def get_species_choice(self):
        choices = []
        if param := self.data.get("species"):
            if param[0] == "_":
                field = "scientific_name"
                code = param[1:]
            else:
                field = "common_name"
                code = param
            choice = (
                Species.objects.filter(species_code=code)
                .values_list("species_code", field)
                .first()
            )
            if choice:
                if param[0] == "_":
                    choice = ("_%s" % choice[0], choice[1])
                else:
                    choice = (choice[0], json.loads(choice[1])[get_language()])
                choices = [choice]
        return choices

    def get_filters(self):
        filters = super().get_filters()
        if species := self.cleaned_data.get("species"):
            if species[0] == "_":
                species = species[1:]
            filters &= Q(species__species_code=species)
        return filters


class DateRangeFilter(FilterForm):
    title = _("By Date")
    identifier = "date-range"

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

    def clean(self):
        start = self.cleaned_data.get("start")
        finish = self.cleaned_data.get("finish")

        if start and finish and start > finish:
            self.add_error("start", self.DATES_SWAPPED)

    def get_filters(self):
        filters = super().get_filters()
        if start := self.cleaned_data.get("start"):
            filters &= Q(date__gte=start)
        if finish := self.cleaned_data.get("finish"):
            filters &= Q(date__lte=finish)
        return filters


class ProtocolFilter(FilterForm):
    title = _("By Protocol")
    identifier = "protocol"

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
            ("P52", _("Oiled Birds")),
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

    def get_filters(self):
        filters = super().get_filters()
        if protocol := self.cleaned_data.get("protocol"):
            filters &= Q(protocol_code=protocol)
        if complete := self.cleaned_data.get("complete"):
            filters &= Q(complete=complete)
        return filters


class ObservationFilter(FilterForm):
    title = _("Options")
    identifier = "observation"

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

    def get_filters(self):
        filters = super().get_filters()
        if approved := self.cleaned_data.get("approved"):
            filters &= Q(approved=approved)
        return filters


class CategoryFilter(FilterForm):
    title = _("By Category")
    identifier = "category"

    category = forms.ChoiceField(
        label=_("Category"),
        choices=Species.Category.choices,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_filters(self):
        filters = super().get_filters()
        if category := self.cleaned_data.get("category"):
            filters &= Q(species__category=category)
        return filters


class ChecklistOrder(FilterForm):
    title = _("Order By")
    identifier = "checklist-order"

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
    title = _("Order By")
    identifier = "observation-order"

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
    title = _("Order By")
    identifier = "species-order"

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("species,started", _("First Seen")),
            ("species,-started", _("Last Seen")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return order.split(",")
        return "species", "started"
