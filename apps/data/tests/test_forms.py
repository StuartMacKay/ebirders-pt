from django import forms
from django.db.models import Q

from data.forms import (
    ChecklistOrder,
    DateRangeFilter,
    HotspotFilter,
    LocationFilter,
    ObservationOrder,
    ObserverFilter,
)


class LocationForm(LocationFilter, forms.Form):
    def __init__(self, *args, **kwargs):
        show_country = kwargs.pop("show_country")
        forms.Form.__init__(self, *args, **kwargs)
        LocationFilter.__init__(self, show_country=show_country)

    def get_filters(self):
        return LocationFilter.get_filters(self)


class ObserverForm(ObserverFilter, forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        ObserverFilter.__init__(self)

    def get_filters(self):
        return ObserverFilter.get_filters(self)


class DateRangeForm(DateRangeFilter, forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        DateRangeFilter.__init__(self)

    def clean(self):
        DateRangeFilter.clean(self)
        return self.cleaned_data

    def get_filters(self):
        return DateRangeFilter.get_filters(self)


class HotspotForm(HotspotFilter, forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        HotspotFilter.__init__(self)

    def get_filters(self):
        return HotspotFilter.get_filters(self)


class ChecklistOrderForm(ChecklistOrder, forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        ChecklistOrder.__init__(self)

    def get_ordering(self):
        return ChecklistOrder.get_ordering(self)


class ObservationOrderForm(ObservationOrder, forms.Form):
    def __init__(self, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        ObservationOrder.__init__(self)

    def get_ordering(self):
        return ObservationOrder.get_ordering(self)


def test_country_field__with_valid_code__form_is_valid(country):
    form = LocationForm(show_country=True, data={"country": country.code})
    assert form.is_valid()


def test_country_field__with_invalid_code__form_is_invalid(country):
    form = LocationForm(show_country=True, data={"country": country.code[::-1]})
    assert not (form.is_valid())


def test_country_field__with_invalid_code__field_error_reported(country):
    form = LocationForm(show_country=True, data={"country": country.code[::-1]})
    form.is_valid()
    assert "country" in form.errors


def test_country_field__with_lowercase_code__field_error_reported(country):
    form = LocationForm(show_country=True, data={"country": country.code.lower()})
    form.is_valid()
    assert "country" in form.errors


def test_country_field__with_valid_code__filter_is_defined(country):
    form = LocationForm(show_country=True, data={"country": country.code})
    form.is_valid()
    assert Q(country__code=country.code) == form.get_filters()


def test_state_field__with_valid_code__form_is_valid(state):
    form = LocationForm(show_country=False, data={"state": state.code})
    assert form.is_valid()


def test_state_field__with_invalid_code__form_is_invalid(state):
    form = LocationForm(show_country=False, data={"state": state.code[::-1]})
    assert not form.is_valid()


def test_state_field__with_invalid_code__field_error_reported(state):
    form = LocationForm(show_country=False, data={"state": state.code[::-1]})
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_lowercase_code__field_error_reported(state):
    form = LocationForm(show_country=False, data={"state": state.code.lower()})
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_other_country__field_error_reported(country, state):
    form = LocationForm(
        show_country=True, data={"country": country.code[::-1], "state": state.code}
    )
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_valid_code__filter_is_defined(state):
    form = LocationForm(show_country=False, data={"state": state.code})
    form.is_valid()
    assert Q(state__code=state.code) == form.get_filters()


def test_county_field__with_valid_code__form_is_valid(county):
    form = LocationForm(show_country=False, data={"county": county.code})
    assert form.is_valid()


def test_county_field__with_invalid_code__form_is_invalid(county):
    form = LocationForm(show_country=False, data={"county": county.code[::-1]})
    assert not form.is_valid()


def test_county_field__with_invalid_code__field_error_reported(county):
    form = LocationForm(show_country=False, data={"county": county.code[::-1]})
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_lowercase_code__field_error_reported(county):
    form = LocationForm(show_country=False, data={"county": county.code.lower()})
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_country__field_error_reported(country, county):
    form = LocationForm(
        show_country=True, data={"country": country.code[::-1], "county": county.code}
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_state__field_error_reported(state, county):
    form = LocationForm(
        show_country=False, data={"state": state.code[::-1], "county": county.code}
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_valid_code__filter_is_defined(county):
    form = LocationForm(show_country=False, data={"county": county.code})
    form.is_valid()
    assert Q(county__code=county.code) == form.get_filters()


def test_location_field__with_valid_code__form_is_valid(location):
    form = LocationForm(show_country=False, data={"location": location.identifier})
    assert form.is_valid()


def test_location_field__with_invalid_code__form_is_invalid(location):
    form = LocationForm(
        show_country=False, data={"location": location.identifier[::-1]}
    )
    assert not form.is_valid()


def test_location_field__with_invalid_code__field_error_reported(location):
    form = LocationForm(
        show_country=False, data={"location": location.identifier[::-1]}
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_lowercase_code__field_error_reported(location):
    form = LocationForm(
        show_country=False, data={"location": location.identifier.lower()}
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_country__field_error_reported(country, location):
    form = LocationForm(
        show_country=True,
        data={"country": country.code[::-1], "location": location.identifier},
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_state__field_error_reported(state, location):
    form = LocationForm(
        show_country=False,
        data={"state": state.code[::-1], "location": location.identifier},
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_county__field_error_reported(county, location):
    form = LocationForm(
        show_country=False,
        data={"country": county.code[::-1], "location": location.identifier},
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_valid_code__filter_is_defined(location):
    form = LocationForm(show_country=False, data={"location": location.identifier})
    form.is_valid()
    assert Q(location__identifier=location.identifier) == form.get_filters()


def test_observer_field__with_valid_code__form_is_valid(observer):
    form = ObserverForm(data={"observer": observer.identifier})
    assert form.is_valid()


def test_observer_field__with_invalid_code__form_is_invalid(observer):
    form = ObserverForm(
        data={"observer": observer.identifier[::-1]}
    )
    assert not form.is_valid()


def test_observer_field__with_invalid_code__field_error_reported(observer):
    form = ObserverForm(
        data={"observer": observer.identifier[::-1]}
    )
    form.is_valid()
    assert "observer" in form.errors


def test_observer_field__with_lowercase_code__field_error_reported(observer):
    form = ObserverForm(
        data={"observer": observer.identifier.lower()}
    )
    form.is_valid()
    assert "observer" in form.errors


def test_observer_field__with_valid_code__filter_is_defined(observer):
    form = ObserverForm(data={"observer": observer.identifier})
    form.is_valid()
    assert Q(observer__identifier=observer.identifier) == form.get_filters()


def test_start_field__invalid_date__field_error_reported(db_no_rollback):
    form = DateRangeForm(data={"start": "2025-01"})
    form.is_valid()
    assert "start" in form.errors


def test_start_field__after_finish_date__field_error_reported(db_no_rollback):
    form = DateRangeForm(
        data={"start": "2025-01-02", "finish": "2025-01-01"}
    )
    form.is_valid()
    assert "start" in form.errors


def test_start_field__with_valid_date__filter_is_defined(db_no_rollback, last_week):
    form = DateRangeForm(data={"start": last_week})
    form.is_valid()
    assert Q(date__gte=last_week) == form.get_filters()


def test_finish_field__invalid_date__field_error_reported(db_no_rollback):
    form = DateRangeForm(data={"finish": "2025-01"})
    form.is_valid()
    assert "finish" in form.errors


def test_finish_field__with_valid_date__filter_is_defined(db_no_rollback, last_week):
    form = DateRangeForm(data={"finish": last_week})
    form.is_valid()
    assert Q(date__lte=last_week) == form.get_filters()


def test_hotspot_field__invalid_boolean__field_error_reported(db_no_rollback):
    form = HotspotForm(data={"hotspot": "Tru"})
    form.is_valid()
    assert "hotspot" in form.errors


def test_hotspot_field__with_valid_data__filter_is_defined(db_no_rollback):
    form = HotspotForm(data={"hotspot": True})
    form.is_valid()
    assert Q(location__hotspot="True") == form.get_filters()


def test_checklist_order_field__default_order(db_no_rollback):
    form = ChecklistOrderForm(data={})
    form.is_valid()
    assert "-started" in form.get_ordering()


def test_checklist_order_field__ordering_set(db_no_rollback):
    form = ChecklistOrderForm(data={"order": "-species_count"})
    form.is_valid()
    assert "-species_count" in form.get_ordering()


def test_checklist_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = ChecklistOrderForm(data={"order": "-species_coun"})
    form.is_valid()
    assert "order" in form.errors


def test_observation_order_field__default_order(db_no_rollback):
    form = ObservationOrderForm(data={})
    form.is_valid()
    assert "-started" in form.get_ordering()


def test_observation_order_field__ordering_set(db_no_rollback):
    form = ObservationOrderForm(data={"order": "-count"})
    form.is_valid()
    assert "-count" in form.get_ordering()


def test_observation_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = ObservationOrderForm(data={"order": "-coun"})
    form.is_valid()
    assert "order" in form.errors
