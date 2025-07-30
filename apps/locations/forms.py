from django import forms
from django.utils.translation import gettext_lazy as _

from dal import autocomplete
from ebird.api.data.models import Country, County, Location, State

from base.forms import FilterForm


class RegionFilter(FilterForm):
    form_id = "region"
    form_title = _("For Region")

    country = forms.ModelMultipleChoiceField(
        label=_("Country"),
        required=False,
        queryset=Country.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="locations:countries",
            attrs={"data-placeholder": _("Select one or more countries")},
        ),
    )

    state = forms.ModelMultipleChoiceField(
        label=_("State"),
        required=False,
        queryset=State.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="locations:states",
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
            url="locations:counties",
            forward=["state", "country"],
            attrs={
                "data-placeholder": _("Select one or more counties"),
            },
        ),
    )


class LocationFilter(FilterForm):
    form_id = "location"
    form_title = _("By Location")

    country = forms.ModelChoiceField(
        label=_("Country"),
        required=False,
        queryset=Country.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="locations:countries",
            attrs={"placeholder": _("Select one or more countries")},
        ),
    )

    state = forms.ModelMultipleChoiceField(
        label=_("State"),
        required=False,
        queryset=State.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="locations:states",
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
            url="locations:counties",
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
            url="locations:locations",
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
