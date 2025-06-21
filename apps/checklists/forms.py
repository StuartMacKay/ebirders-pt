from django import forms
from django.db.models import Q

from data.forms import (
    ChecklistOrder,
    DateRangeFilter,
    HotspotFilter,
    LocationFilter,
    ObserverFilter,
)


class ChecklistFilterForm(
    LocationFilter,
    ObserverFilter,
    DateRangeFilter,
    HotspotFilter,
    ChecklistOrder,
    forms.Form,
):
    def __init__(self, *args, **kwargs):
        show_country = kwargs.pop("show_country")
        forms.Form.__init__(self, *args, **kwargs)
        LocationFilter.__init__(self, show_country=show_country)
        ObserverFilter.__init__(self)
        DateRangeFilter.__init__(self)
        HotspotFilter.__init__(self)
        ChecklistOrder.__init__(self)

    def clean(self):
        DateRangeFilter.clean(self)
        return self.cleaned_data

    def get_filters(self):
        filters = Q()
        filters &= LocationFilter.get_filters(self)
        filters &= ObserverFilter.get_filters(self)
        filters &= DateRangeFilter.get_filters(self)
        filters &= HotspotFilter.get_filters(self)
        return filters

    def get_ordering(self):
        return ChecklistOrder.get_ordering(self)
