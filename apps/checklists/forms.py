from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.forms import FilterForm


class Protocol(models.TextChoices):
    INCIDENTAL = "P20", _("Incidental")
    STATIONARY = "P21", _("Stationary")
    TRAVELING = "P22", _("Traveling")
    AREA = "P23", _("Area")
    BANDING = "P33", _("Banding")
    NOCTURNAL = "P54", _("Nocturnal Flight Call Count")
    PELAGIC = "P60", _("eBird Pelagic Protocol")
    HISTORICAL = "P62", _("Historical")
    COMMON_BIRD_SURVEY = ("P67", _("Common Bird Survey"))
    SEABIRD_CENSUS = ("P68", _("Seabird Census"))


class ProtocolFilter(FilterForm):
    form_id = "protocol"
    form_title = _("For Protocol")

    protocol = forms.ChoiceField(
        label=_("Protocol"),
        choices=[
            ("", _("All")),
        ]
        + Protocol.choices,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    complete = forms.ChoiceField(
        label=_("Status"),
        choices=(
            ("", _("All")),
            ("True", _("Complete")),
            ("False", _("Incomplete")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    filters = {"protocol": "protocol_code", "complete": "complete"}


class ChecklistOrder(FilterForm):
    form_id = "checklist-order"
    form_title = _("Order By")

    order = forms.ChoiceField(
        label=_("Ordering"),
        choices=(
            ("-started", _("Most recent first")),
            ("-species_count,-started", _("Number of species")),
        ),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def get_ordering(self):
        if order := self.cleaned_data.get("order"):
            return order.split(",")
        return ("-started",)
