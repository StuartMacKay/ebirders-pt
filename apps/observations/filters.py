from django.forms import DateInput
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

import django_filters

from dal import autocomplete

from data.models import Country, County, Location, Observation, Observer, Species, State


class ObservationFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        label=_("Country"),
        field_name="country__code",
        widget=autocomplete.Select2(
            url="data:countries",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    state = django_filters.CharFilter(
        label=_("State"),
        field_name="state__code",
        widget=autocomplete.Select2(
            url="data:states",
            forward=["country"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    county = django_filters.CharFilter(
        label=_("County"),
        field_name="county__code",
        widget=autocomplete.Select2(
            url="data:counties",
            forward=["state"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    location = django_filters.CharFilter(
        label=_("Location"),
        field_name="location__identifier",
        widget=autocomplete.Select2(
            url="data:locations",
            forward=["county"],
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    observer = django_filters.CharFilter(
        label=_("Observer"),
        field_name="observer__identifier",
        widget=autocomplete.Select2(
            url="data:observers",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    species = django_filters.CharFilter(
        label=_("Species"),
        method="filter_species",
        widget=autocomplete.Select2(
            url="data:species",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )
    start = django_filters.DateFilter(
        label=_("From"),
        field_name="date",
        lookup_expr="gte",
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    finish = django_filters.DateFilter(
        label=_("Until"),
        field_name="date",
        lookup_expr="lte",
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Observation
        fields = ("country", "state", "county", "location", "observer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if Country.objects.all().count() == 1:
            del self.filters["country"]

        if code := self.data.get("country"):
            self.declared_filters[
                "country"
            ].field.widget.choices = Country.objects.filter(code=code).values_list(
                "code", "name"
            )

        if code := self.data.get("state"):
            self.declared_filters["state"].field.widget.choices = State.objects.filter(
                code=code
            ).values_list("code", "name")

        if code := self.data.get("county"):
            self.declared_filters[
                "county"
            ].field.widget.choices = County.objects.filter(code=code).values_list(
                "code", "name"
            )

        if identifier := self.data.get("location"):
            self.declared_filters[
                "location"
            ].field.widget.choices = Location.objects.filter(
                identifier=identifier
            ).values_list("identifier", "name")

        if identifier := self.data.get("observer"):
            self.declared_filters[
                "observer"
            ].field.widget.choices = Observer.objects.filter(
                identifier=identifier
            ).values_list("identifier", "name")

        if param := self.data.get("species"):

            if param[0] == "_":
                field = "scientific_name"
                code = param[1:]
                prefix = "_"
            else:
                field = "data__common_name__%s" % get_language()
                code = param
                prefix = ""

            choice = Species.objects.filter(
                species_code=code
            ).values_list("species_code", field).first()

            if choice:
                choice = ("%s%s" % (prefix, choice[0]), choice[1])
                self.declared_filters["species"].field.widget.choices = [choice]
            else:
                self.declared_filters["species"].field.widget.choices = []

    def filter_species(self, queryset, field_name, value):
        if not value:
            return queryset
        if value[0] == '_':
            value = value[1:]
        return queryset.filter(species__species_code=value)
