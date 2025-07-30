from django import forms
from django.utils.translation import gettext_lazy as _

from dal import autocomplete
from ebird.api.data.models import Observer

from base.forms import FilterForm


class ObserverFilter(FilterForm):
    form_id = "observer"
    form_title = _("By Observer")

    observer = forms.ModelChoiceField(
        label=_("Observer"),
        required=False,
        queryset=Observer.objects.all(),
        widget=autocomplete.Select2(
            url="observers:observers",
            attrs={"class": "form-select", "data-theme": "bootstrap-5"},
        ),
    )

    filters = {
        "observer": "observer",
    }
