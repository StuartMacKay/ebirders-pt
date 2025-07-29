import datetime as dt
import re

from django import forms
from django.utils.translation import gettext_lazy as _

from dal import autocomplete
from dateutil.relativedelta import relativedelta
from ebird.api.data.models import Country, County, State


class FilterForm(forms.Form):
    form_id = None
    form_title = None

    def get_params(self):
        return {field: value for field, value in self.cleaned_data.items() if value}


class RegionFilter(FilterForm):
    form_id = "region"
    form_title = _("For Region")

    country = forms.ModelMultipleChoiceField(
        label=_("Country"),
        required=False,
        queryset=Country.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="filters:countries",
            attrs={"data-placeholder": _("Select one or more countries")},
        ),
    )

    state = forms.ModelMultipleChoiceField(
        label=_("State"),
        required=False,
        queryset=State.objects.all(),
        widget=autocomplete.Select2Multiple(
            url="filters:states",
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
            url="filters:counties",
            forward=["state", "country"],
            attrs={
                "data-placeholder": _("Select one or more counties"),
            },
        ),
    )


class WeekFilter(FilterForm):
    form_id = "week"
    form_title = _("For Week")

    week = forms.CharField(
        label=_("Week"),
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "week",
                "class": "form-control",
                "placeholder": _("Enter week, e.g. 2025-W01"),
            }
        ),
    )

    INVALID_FORMAT = _("Enter a week in the form YYYY-WDD, e.g. 2025-W01")

    def clean_week(self):
        value = self.cleaned_data["week"]
        if not re.match("\d4-W\d2", value):
            raise forms.ValidationError(self.INVALID_FORMAT)
        return value

    def clean(self):
        cleaned_data = super().clean()
        if value := cleaned_data.get("week"):
            parsed_date = dt.datetime.strptime("%s-1" % value, "%Y-W%W-%w").date()
            # python's week numbers start at zero, html's start at one.
            finish_date = parsed_date - dt.timedelta(days=1)
            start_date = finish_date - dt.timedelta(days=6)
            cleaned_data["start"] = start_date
            cleaned_data["finish"] = finish_date
            cleaned_data["year"] = parsed_date.year
            cleaned_data["week"] = parsed_date.isocalendar().week
        return cleaned_data


class MonthFilter(FilterForm):
    form_id = "month"
    form_title = _("For Month")

    month = forms.CharField(
        label=_("Month"),
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "month",
                "class": "form-control",
                "placeholder": _("Enter month, e.g. 2025-01"),
            }
        ),
    )

    INVALID_FORMAT = _("Enter a month in the form YYYY-MM, e.g. 2025-01")

    def clean_month(self):
        value = self.cleaned_data["month"]
        if not re.match("\d4-\d2", value):
            raise forms.ValidationError(self.INVALID_FORMAT)
        return value

    def clean(self):
        cleaned_data = super().clean()
        if value := cleaned_data.get("month"):
            start_date = dt.datetime.strptime(value, "%Y-%m").date()
            finish_date = start_date + relativedelta(months=1, days=-1)
            cleaned_data["start"] = start_date
            cleaned_data["finish"] = finish_date
            cleaned_data["year"] = start_date.year
            cleaned_data["month"] = start_date.month
        return cleaned_data
