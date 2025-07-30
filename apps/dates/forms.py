import datetime as dt
import re

from django import forms
from django.utils.translation import gettext_lazy as _

from dateutil.relativedelta import relativedelta

from base.forms import FilterForm


class DateRangeFilter(FilterForm):
    form_id = "date-range"
    form_title = _("By Date")

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

    filters = {
        "start": "date__gte",
        "finish": "date__lte",
    }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start")
        finish = cleaned_data.get("finish")
        if start and finish and start > finish:
            self.add_error("start", self.DATES_SWAPPED)
        return cleaned_data


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
        if value and not re.match(r"\d{4}-W\d{2}", value):
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
        if value and not re.match(r"\d{4}-\d{2}", value):
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
