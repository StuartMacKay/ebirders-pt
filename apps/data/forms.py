import json

from django import forms
from django.db.models import Q
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from data.models import Country, County, Location, Observer, Species, State


class LocationFilter:
    def __init__(self, show_country):
        fields = getattr(self, "fields")

        if show_country:
            fields["country"] = forms.ChoiceField(
                label=_("Country"),
                choices=self.get_country_choices(),
                required=False,
                widget=autocomplete.Select2(
                    url="data:countries",
                    attrs={"class": "form-select", "data-theme": "bootstrap-5"},
                ),
            )

        fields["state"] = forms.ChoiceField(
            label=_("State"),
            choices=self.get_state_choices(),
            required=False,
            widget=autocomplete.Select2(
                url="data:states",
                forward=["country"],
                attrs={"class": "form-select", "data-theme": "bootstrap-5"},
            ),
        )

        fields["county"] = forms.ChoiceField(
            label=_("County"),
            choices=self.get_county_choices(),
            required=False,
            widget=autocomplete.Select2(
                url="data:counties",
                forward=["state"],
                attrs={"class": "form-select", "data-theme": "bootstrap-5"},
            ),
        )

        fields["location"] = forms.ChoiceField(
            label=_("Location"),
            choices=self.get_location_choices(),
            required=False,
            widget=autocomplete.Select2(
                url="data:locations",
                forward=["county"],
                attrs={"class": "form-select", "data-theme": "bootstrap-5"},
            ),
        )

    def get_country_choices(self):
        choices = []
        if country := getattr(self, "data").get("country"):
            choices = Country.objects.filter(code=country).values_list("code", "name")
        return choices

    def get_state_choices(self):
        data = getattr(self, "data")
        choices = []
        if state := data.get("state"):
            choices = State.objects.filter(code=state).values_list("code", "name")
            if country := data.get("country"):
                choices = choices.filter(code__startswith=country)
        return choices

    def get_county_choices(self):
        data = getattr(self, "data")
        choices = []
        if county := data.get("county"):
            choices = County.objects.filter(code=county).values_list("code", "name")
            if state := data.get("state"):
                choices = choices.filter(code__startswith=state)
            if country := data.get("country"):
                choices = choices.filter(code__startswith=country)
        return choices

    def get_location_choices(self):
        data = getattr(self, "data")
        choices = []
        if location := data.get("location"):
            choices = (
                Location.objects.all()
                .filter(identifier=location)
                .values_list("identifier", "name")
            )
            if county := data.get("county"):
                choices = choices.filter(county__code=county)
            if state := data.get("state"):
                choices = choices.filter(state__code=state)
            if country := data.get("country"):
                choices = choices.filter(country__code=country)
        return choices

    def get_filters(self):
        cleaned_data = getattr(self, "cleaned_data")
        filters = Q()
        if country := cleaned_data.get("country"):
            filters &= Q(country__code=country)
        if state := cleaned_data.get("state"):
            filters &= Q(state__code=state)
        if county := cleaned_data.get("county"):
            filters &= Q(county__code=county)
        if location := cleaned_data.get("location"):
            filters &= Q(location__identifier=location)
        return filters


class ObserverFilter:
    def __init__(self):
        getattr(self, "fields")["observer"] = forms.ChoiceField(
            label=_("Observer"),
            choices=self.get_observer_choices(),
            required=False,
            widget=autocomplete.Select2(
                url="data:observers",
                attrs={"class": "form-select", "data-theme": "bootstrap-5"},
            ),
        )

    def get_observer_choices(self):
        choices = []
        if observer := getattr(self, "data").get("observer"):
            choices = Observer.objects.filter(identifier=observer).values_list("identifier", "name")
        return choices

    def get_filters(self):
        filters = Q()
        if observer := getattr(self, "cleaned_data").get("observer"):
            filters &= Q(observer__identifier=observer)
        return filters


class SpeciesFilter:
    def __init__(self):
        getattr(self, "fields")["species"] = forms.ChoiceField(
            label=_("Species"),
            choices=self.get_species_choices(),
            required=False,
            widget=autocomplete.Select2(
                url="data:species",
                attrs={"class": "form-select", "data-theme": "bootstrap-5"},
            ),
        )

    def get_species_choices(self):
        choices = []
        if param := getattr(self, "data").get("species"):
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
        if species := getattr(self, "cleaned_data").get("species"):
            if species[0] == "_":
                species = species[1:]
            filters &= Q(species__species_code=species)
        return filters


class DateRangeFilter:
    DATES_SWAPPED = _("This date is later than the until date.")

    def __init__(self):
        fields = getattr(self, "fields")
        fields["start"] = forms.DateField(
            label=_("From"),
            required=False,
            widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        )
        fields["finish"] = forms.DateField(
            label=_("Until"),
            required=False,
            widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        )

    def clean(self):
        cleaned_data = getattr(self, "cleaned_data")
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")

        if start and finish and start > finish:
            getattr(self, "add_error")("start", self.DATES_SWAPPED)

    def get_filters(self):
        cleaned_data = getattr(self, "cleaned_data")
        filters = Q()
        if start := cleaned_data.get("start"):
            filters &= Q(date__gte=start)
        if finish := cleaned_data.get("finish"):
            filters &= Q(date__lte=finish)
        return filters


class HotspotFilter:
    def __init__(self):
        getattr(self, "fields")["hotspot"] = forms.ChoiceField(
            label=_("Hotspots only"),
            choices=(
                ("", _("No")),
                ("True", _("Yes")),
            ),
            required=False,
            widget=forms.Select(attrs={"class": "form-control"}),
        )

    def get_filters(self):
        filters = Q()
        if hotspot := getattr(self, "cleaned_data").get("hotspot"):
            filters &= Q(location__hotspot=hotspot)
        return filters


class CategoryFilter:
    def __init__(self):
        getattr(self, "fields")["category"] = forms.ChoiceField(
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
        if category := getattr(self, "cleaned_data").get("category"):
            filters &= Q(species__category=category)
        return filters


class ChecklistOrder:
    def __init__(self):
        getattr(self, "fields")["order"] = forms.ChoiceField(
            label=_("Ordering"),
            choices=(
                ("", _("Most recent first")),
                ("species_count", _("Number of species")),
                ("-species_count", _("Number of species (descending)")),
            ),
            required=False,
            widget=forms.Select(attrs={"class": "form-control"}),
        )

    def get_ordering(self):
        if order := getattr(self, "cleaned_data").get("order"):
            return (order,)
        return ("-started",)


class ObservationOrder:
    def __init__(self):
        getattr(self, "fields")["order"] = forms.ChoiceField(
            label=_("Ordering"),
            choices=(
                ("", _("Most recent first")),
                ("count", _("Count")),
                ("-count", _("Count (descending)")),
            ),
            required=False,
            widget=forms.Select(attrs={"class": "form-control"}),
        )

    def get_ordering(self):
        if order := getattr(self, "cleaned_data").get("order"):
            return (order,)
        return ("-started",)


class SeenOrder:
    def __init__(self):
        getattr(self, "fields")["order"] = forms.ChoiceField(
            label=_("Ordering"),
            choices=(
                ("seen", _("First Seen")),
                ("-seen", _("Last Seen")),
            ),
            required=False,
            widget=forms.Select(attrs={"class": "form-control"}),
        )

    def get_ordering(self):
        if order := getattr(self, "cleaned_data").get("order"):
            if order == "-seen":
                return ("species", "-date")
        return ("species", "date")
