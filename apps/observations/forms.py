from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import FilterForm


class ObservationFilter(FilterForm):
    form_id = "observation"
    form_title = _("Options")

    approved = forms.ChoiceField(
        label=_("Status"),
        choices=(
            ("", _("All")),
            ("True", _("Accepted")),
            ("False", _("Rejected")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    audio = forms.ChoiceField(
        label=_("With audio"),
        choices=(
            ("", _("All")),
            ("True", _("Yes")),
            ("False", _("No")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    photo = forms.ChoiceField(
        label=_("With photos"),
        choices=(
            ("", _("All")),
            ("True", _("Yes")),
            ("False", _("No")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    video = forms.ChoiceField(
        label=_("With video"),
        choices=(
            ("", _("All")),
            ("True", _("Yes")),
            ("False", _("No")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    filters = {
        "approved": "approved",
        "audio": "audio",
        "photo": "photo",
        "video": "video",
    }


class ObservationOrder(FilterForm):
    form_id = "observation-order"
    form_title = _("Order By")

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("-started", _("Most recent first")),
            ("-count", _("Highest count first")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return (order,)
        return ("-started",)
