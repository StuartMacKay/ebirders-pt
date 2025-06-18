import re

from django import forms
from django.utils.translation import gettext_lazy as _

from ebird.codes.locations import (
    is_country_code,
    is_county_code,
    is_location_code,
    is_state_code,
)

from data.models import Country, County, Location, Observer, State

INVALID_COUNTRY_CODE = _("Please select a country.")
INVALID_STATE_CODE = _("Please select a state.")
INVALID_COUNTY_CODE = _("Please select a county.")
INVALID_LOCATION_CODE = _("Please select a location.")
INVALID_OBSERVER_CODE = _("Please select an observer.")
DATES_SWAPPED = _("This date is later than the until date.")

OBSERVER_CODE = re.compile(r"^USER\d+$")


def is_observer_code(code: str) -> bool:
    """Is the code for an Observer, e.g. 'USER123456'."""
    return OBSERVER_CODE.match(code) is not None


class ChecklistFilterForm(forms.Form):
    """
    ChecklistFilterForm is used to provide feedback if there are any invalid
    codes passed in the querystring for the ChecklistFilterSet.

    Since the filtering of Checklists is based on the user selecting codes
    from autocomplete lists, it is unlikely incorrect codes would be entered.
    However if the querystring parameters are edited directly or if a link
    to the checklists page is incorrect, then feedback on which code or
    identifier is incorrect is useful.

    """
    def clean_country(self):
        if code := self.cleaned_data["country"]:
            if not is_country_code(code):
                raise forms.ValidationError(INVALID_COUNTRY_CODE)
            if not Country.objects.filter(code=code).exists():
                raise forms.ValidationError(INVALID_COUNTRY_CODE)
        return code

    def clean_state(self):
        if code := self.cleaned_data["state"]:
            if not is_state_code(code):
                raise forms.ValidationError(INVALID_STATE_CODE)
            if not State.objects.filter(code=code).exists():
                raise forms.ValidationError(INVALID_STATE_CODE)
        return code

    def clean_county(self):
        if code := self.cleaned_data["county"]:
            if not is_county_code(code):
                raise forms.ValidationError(INVALID_COUNTY_CODE)
            if not County.objects.filter(code=code).exists():
                raise forms.ValidationError(INVALID_COUNTY_CODE)
        return code

    def clean_location(self):
        if identifier := self.cleaned_data["location"]:
            if not is_location_code(identifier):
                raise forms.ValidationError(INVALID_LOCATION_CODE)
            if not Location.objects.filter(identifier=identifier).exists():
                raise forms.ValidationError(INVALID_LOCATION_CODE)
        return identifier

    def clean_observer(self):
        if identifier := self.cleaned_data["observer"]:
            if not is_observer_code(identifier):
                raise forms.ValidationError(INVALID_OBSERVER_CODE)
            if not Observer.objects.filter(identifier=identifier).exists():
                raise forms.ValidationError(INVALID_OBSERVER_CODE)
        return identifier

    def clean(self):
        start = self.cleaned_data.get("start")
        finish = self.cleaned_data.get("finish")

        if start and finish and start > finish:
            self.add_error("start", DATES_SWAPPED)
