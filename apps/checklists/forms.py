from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from dal import autocomplete

from data.models import Country, County, Location, Observer, State

DATES_SWAPPED = _("This date is later than the until date.")


class ChecklistFilterForm(forms.Form):
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
    location = forms.ChoiceField(
        label=_("Location"),
        required=False,
        widget=autocomplete.Select2(
            url="data:locations",
            forward=["county"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    observer = forms.ChoiceField(
        label=_("Observer"),
        required=False,
        widget=autocomplete.Select2(
            url="data:observers",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
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
    hotspot = forms.ChoiceField(
        label=_("Hotspots only"),
        choices=(
            ("", _("No")),
            ("True", _("Yes")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
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

    def __init__(self, *args, **kwargs):
        show_country = kwargs.pop("show_country")
        super().__init__(*args, **kwargs)

        if not show_country:
            del self.fields["country"]
        else:
            self.fields["country"].choices = self.get_country_choices()

        self.fields["state"].choices = self.get_state_choices()
        self.fields["county"].choices = self.get_county_choices()
        self.fields["location"].choices = self.get_location_choices()
        self.fields["observer"].choices = self.get_observer_choices()

    def get_country_choices(self):
        queryset = Country.objects.all().values_list("code", "name")
        if country := self.data.get("country"):
            queryset = queryset.filter(code=country)
        return queryset

    def get_state_choices(self):
        queryset = State.objects.all().values_list("code", "name")
        if country := self.data.get("country"):
            queryset = queryset.filter(code__startswith=country)
        if state := self.data.get("state"):
            queryset = queryset.filter(code=state)
        return queryset

    def get_county_choices(self):
        queryset = County.objects.all().values_list("code", "name")
        if country := self.data.get("country"):
            queryset = queryset.filter(code__startswith=country)
        if state := self.data.get("state"):
            queryset = queryset.filter(code__startswith=state)
        if county := self.data.get("county"):
            queryset = queryset.filter(code=county)
        return queryset

    def get_location_choices(self):
        queryset = Location.objects.all().values_list("identifier", "name")
        if country := self.data.get("country"):
            queryset = queryset.filter(country__code=country)
        if state := self.data.get("state"):
            queryset = queryset.filter(state__code=state)
        if county := self.data.get("county"):
            queryset = queryset.filter(county__code=county)
        if location := self.data.get("location"):
            queryset = queryset.filter(identifier=location)
        return queryset

    def get_observer_choices(self):
        queryset = Observer.objects.all().values_list("identifier", "name")
        if observer := self.data.get("observer"):
            queryset = queryset.filter(identifier=observer)
        return queryset

    def clean(self):
        start = self.cleaned_data.get("start")
        finish = self.cleaned_data.get("finish")

        if start and finish and start > finish:
            self.add_error("start", DATES_SWAPPED)

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
        if observer := self.cleaned_data.get("observer"):
            filters &= Q(observer__identifier=observer)
        if start := self.cleaned_data.get("start"):
            filters &= Q(date__gte=start)
        if finish := self.cleaned_data.get("finish"):
            filters &= Q(date__lte=finish)
        if hotspot := self.cleaned_data.get("hotspot"):
            filters &= Q(location__hotspot=hotspot)
        return filters

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return (order,)
        return ("-started",)
