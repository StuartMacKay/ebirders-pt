from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from data.models import Country, County, Location, Observer, State


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
        data = getattr(self, "data")
        queryset = Country.objects.all().values_list("code", "name")
        if country := data.get("country"):
            queryset = queryset.filter(code=country)
        return queryset

    def get_state_choices(self):
        data = getattr(self, "data")
        queryset = State.objects.all().values_list("code", "name")
        if country := data.get("country"):
            queryset = queryset.filter(code__startswith=country)
        if state := data.get("state"):
            queryset = queryset.filter(code=state)
        return queryset

    def get_county_choices(self):
        data = getattr(self, "data")
        queryset = County.objects.all().values_list("code", "name")
        if country := data.get("country"):
            queryset = queryset.filter(code__startswith=country)
        if state := data.get("state"):
            queryset = queryset.filter(code__startswith=state)
        if county := data.get("county"):
            queryset = queryset.filter(code=county)
        return queryset

    def get_location_choices(self):
        data = getattr(self, "data")
        queryset = Location.objects.all().values_list("identifier", "name")
        if country := data.get("country"):
            queryset = queryset.filter(country__code=country)
        if state := data.get("state"):
            queryset = queryset.filter(state__code=state)
        if county := data.get("county"):
            queryset = queryset.filter(county__code=county)
        if location := data.get("location"):
            queryset = queryset.filter(identifier=location)
        return queryset

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
        queryset = Observer.objects.all().values_list("identifier", "name")
        if observer := getattr(self, "data").get("observer"):
            queryset = queryset.filter(identifier=observer)
        return queryset

    def get_filters(self):
        filters = Q()
        if observer := getattr(self, "cleaned_data").get("observer"):
            filters &= Q(observer__identifier=observer)
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
