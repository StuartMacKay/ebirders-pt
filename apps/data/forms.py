import json

from django import forms
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from data.models import Country, County, Location, Observer, Species, State


class LocationFilter(forms.Form):
    title = _("By Location")
    identifier = "location"

    country = forms.ChoiceField(
        label=_("Country"),
        required=False,
        widget=autocomplete.Select2(
            url="data:countries",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    state = forms.ChoiceField(
        label=_("State"),
        required=False,
        widget=autocomplete.Select2(
            url="data:states",
            forward=["country"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    county = forms.ChoiceField(
        label=_("County"),
        required=False,
        widget=autocomplete.Select2(
            url="data:counties",
            forward=["state"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    location= forms.ChoiceField(
        label=_("Location"),
        required=False,
        widget=autocomplete.Select2(
            url="data:locations",
            forward=["county"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
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
        super().__init__(*args, **kwargs)
        if self.is_bound:
            self.fields["country"].choices = self.get_country_choice()
            self.fields["state"].choices = self.get_state_choice()
            self.fields["county"].choices = self.get_county_choice()
            self.fields["location"].choices = self.get_location_choice()

    def get_country_choice(self):
        choices = []
        if country := self.data.get("country"):
            choices = Country.objects.filter(code=country).values_list("code", "name")
        return choices

    def get_state_choice(self):
        choices = []
        if state := self.data.get("state"):
            choices = State.objects.filter(code=state).values_list("code", "name")
            if country := self.data.get("country"):
                choices = choices.filter(code__startswith=country)
        return choices

    def get_county_choice(self):
        choices = []
        if county := self.data.get("county"):
            choices = County.objects.filter(code=county).values_list("code", "name")
            if state := self.data.get("state"):
                choices = choices.filter(code__startswith=state)
            if country := self.data.get("country"):
                choices = choices.filter(code__startswith=country)
        return choices

    def get_location_choice(self):
        choices = []
        if location := self.data.get("location"):
            choices = (
                Location.objects.all()
                .filter(identifier=location)
                .values_list("identifier", "name")
            )
            if county := self.data.get("county"):
                choices = choices.filter(county__code=county)
            if state := self.data.get("state"):
                choices = choices.filter(state__code=state)
            if country := self.data.get("country"):
                choices = choices.filter(country__code=country)
        return choices

    def get_filters(self):
        filters = Q()
        if country := self.cleaned_data.get("country"):
            filters &= Q(country__code=country)
        if state := self.cleaned_data.get("state"):
            filters &= Q(state__code=state)
        if county := self.cleaned_data.get("county"):
            filters &= Q(county__code=county)
        if location := self.cleaned_data.get("location"):
            filters &= Q(location__identifier=location)
        if hotspot := self.cleaned_data.get("hotspot"):
            filters &= Q(location__hotspot=hotspot)
        return filters

    def get_ordering(self):
        return []


class ObserverFilter(forms.Form):
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
        filters = Q()
        if observer := self.cleaned_data.get("observer"):
            filters &= Q(observer__identifier=observer)
        return filters

    def get_ordering(self):
        return []


class SpeciesFilter(forms.Form):
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
        filters = Q()
        if species := self.cleaned_data.get("species"):
            if species[0] == "_":
                species = species[1:]
            filters &= Q(species__species_code=species)
        return filters

    def get_ordering(self):
        return []


class DateRangeFilter(forms.Form):
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
        filters = Q()
        if start := self.cleaned_data.get("start"):
            filters &= Q(date__gte=start)
        if finish := self.cleaned_data.get("finish"):
            filters &= Q(date__lte=finish)
        return filters

    def get_ordering(self):
        return []


class CategoryFilter(forms.Form):
    title = _("By Category")
    identifier = "category"

    category = forms.ChoiceField(
        label=_("Category"),
        choices=(
            ("species", _("Species")),
            ("issf", _("Subspecies")),
            ("domestic", _("Domestic")),
            ("hybrid", _("Hybrid")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_filters(self):
        filters = Q()
        if category := self.cleaned_data.get("category"):
            filters &= Q(species__category=category)
        return filters

    def get_ordering(self):
        return []


class ChecklistOrder(forms.Form):
    title = _("Order By")
    identifier = "checklist-order"

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("", _("Most recent first")),
            ("species_count", _("Number of species")),
            ("-species_count", _("Number of species (descending)")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_filters(self):
        return Q()

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return (order,)
        return ("-started",)


class ObservationOrder(forms.Form):
    title = _("Order By")
    identifier = "observation-order"

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("", _("Most recent first")),
            ("count", _("Count")),
            ("-count", _("Count (descending)")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_filters(self):
        return Q()

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return (order,)
        return ("-started",)


class SeenOrder(forms.Form):
    title = _("Order By")
    identifier = "seen-order"

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("seen", _("First Seen")),
            ("-seen", _("Last Seen")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_filters(self):
        return Q()

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            if order == "-seen":
                return "species", "-date"
        return "species", "date"
