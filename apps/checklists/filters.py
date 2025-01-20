import django_filters
from dal import autocomplete
from django.utils.translation import gettext_lazy as _
from ebird.checklists.models import Checklist

from .queries import country_choice, state_choice, county_choice


class ChecklistFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        label=_("Country"),
        field_name="location__country_code",
        widget=autocomplete.Select2(url="checklists:countries", attrs={"class": "form-select", "data-theme": "bootstrap-5"}),
    )
    state = django_filters.CharFilter(
        label=_("State"),
        field_name="location__state_code",
        widget=autocomplete.Select2(url="checklists:states", forward=["country"], attrs={"class": "form-select", "data-theme": "bootstrap-5"}),
    )
    county = django_filters.CharFilter(
        label=_("County"),
        field_name="location__county_code",
        widget=autocomplete.Select2(url="checklists:counties", forward=["state"], attrs={"class": "form-select", "data-theme": "bootstrap-5"}),
    )

    class Meta:
        model = Checklist
        fields = ("country", "state", "county")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if country := self.data.get("country"):
            self.declared_filters["country"].field.widget.choices = [
                country_choice(country)
            ]

        if state := self.data.get("state"):
            self.declared_filters["state"].field.widget.choices = [state_choice(state)]

        if county := self.data.get("county"):
            self.declared_filters["county"].field.widget.choices = [
                county_choice(county)
            ]
