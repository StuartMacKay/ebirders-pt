from django import forms
from django.utils.translation import gettext_lazy as _

from base.forms import FilterForm


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
