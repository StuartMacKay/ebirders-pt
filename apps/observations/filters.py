import django_filters
from dal import autocomplete
from django.utils.translation import gettext_lazy as _
from checklists.models import Observation

from .queries import (
    country_choice,
    district_choice,
    county_choice,
    location_choice,
    observer_choice,
    species_choice,
)


class ObservationFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        label=_("Country"),
        field_name="location__country__code",
        widget=autocomplete.Select2(
            url="observations:countries",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    district = django_filters.CharFilter(
        label=_("District"),
        field_name="location__district__code",
        widget=autocomplete.Select2(
            url="observations:districts",
            forward=["country"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    county = django_filters.CharFilter(
        label=_("County"),
        field_name="location__county__code",
        widget=autocomplete.Select2(
            url="observations:counties",
            forward=["country", "district"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    location = django_filters.CharFilter(
        label=_("Location"),
        field_name="location__identifier",
        widget=autocomplete.Select2(
            url="observations:locations",
            forward=["country", "district", "county"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    observer = django_filters.CharFilter(
        label=_("Observer"),
        field_name="observer__name",
        widget=autocomplete.Select2(
            url="observations:observers",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    species = django_filters.CharFilter(
        label=_("Species"),
        field_name="species__species_code",
        widget=autocomplete.Select2(
            url="observations:species",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    class Meta:
        model = Observation
        fields = ("location", "observer", "species")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if country := self.data.get("country"):
            self.declared_filters["country"].field.widget.choices = [
                country_choice(country)
            ]

        if state := self.data.get("district"):
            self.declared_filters["district"].field.widget.choices = [district_choice(state)]

        if county := self.data.get("county"):
            self.declared_filters["county"].field.widget.choices = [
                county_choice(county)
            ]

        if location := self.data.get("location"):
            self.declared_filters["location"].field.widget.choices = [
                location_choice(location)
            ]

        if name := self.data.get("observer"):
            self.declared_filters["observer"].field.widget.choices = [
                observer_choice(name)
            ]

        if code := self.data.get("species"):
            self.declared_filters["species"].field.widget.choices = [
                species_choice(code)
            ]
