from django import forms
from django.db.models import Q

from data.forms import (
    DateRangeFilter,
    HotspotFilter,
    LocationFilter,
    ObservationOrder,
    ObserverFilter,
    SpeciesFilter,
)


class ObservationFilterForm(
    LocationFilter,
    ObserverFilter,
    DateRangeFilter,
    HotspotFilter,
    SpeciesFilter,
    ObservationOrder,
    forms.Form,
):
    def __init__(self, *args, **kwargs):
        show_country = kwargs.pop("show_country")
        forms.Form.__init__(self, *args, **kwargs)
        LocationFilter.__init__(self, show_country=show_country)
        ObserverFilter.__init__(self)
        DateRangeFilter.__init__(self)
        SpeciesFilter.__init__(self)
        ObservationOrder.__init__(self)

    def clean(self):
        DateRangeFilter.clean(self)
        return self.cleaned_data

    def get_filters(self):
        filters = Q()
        filters &= LocationFilter.get_filters(self)
        filters &= ObserverFilter.get_filters(self)
        filters &= DateRangeFilter.get_filters(self)
        filters &= SpeciesFilter.get_filters(self)
        return filters

    def get_ordering(self):
        return ObservationOrder.get_ordering(self)
