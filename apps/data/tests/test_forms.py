from django.db.models import Q

from data.forms import (
    CategoryFilter,
    ChecklistOrder,
    DateRangeFilter,
    HotspotFilter,
    LocationFilter,
    ObservationOrder,
    ObserverFilter,
    SeenOrder,
)


def test_country_field__with_valid_code__form_is_valid(country):
    form = LocationFilter(show_country=True, data={"country": country.code})
    assert form.is_valid()


def test_country_field__with_invalid_code__form_is_invalid(country):
    form = LocationFilter(show_country=True, data={"country": country.code[::-1]})
    assert not (form.is_valid())


def test_country_field__with_invalid_code__field_error_reported(country):
    form = LocationFilter(show_country=True, data={"country": country.code[::-1]})
    form.is_valid()
    assert "country" in form.errors


def test_country_field__with_lowercase_code__field_error_reported(country):
    form = LocationFilter(show_country=True, data={"country": country.code.lower()})
    form.is_valid()
    assert "country" in form.errors


def test_country_field__with_valid_code__filter_is_defined(country):
    form = LocationFilter(show_country=True, data={"country": country.code})
    form.is_valid()
    assert Q(country__code=country.code) == form.get_filters()


def test_state_field__with_valid_code__form_is_valid(state):
    form = LocationFilter(show_country=False, data={"state": state.code})
    assert form.is_valid()


def test_state_field__with_invalid_code__form_is_invalid(state):
    form = LocationFilter(show_country=False, data={"state": state.code[::-1]})
    assert not form.is_valid()


def test_state_field__with_invalid_code__field_error_reported(state):
    form = LocationFilter(show_country=False, data={"state": state.code[::-1]})
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_lowercase_code__field_error_reported(state):
    form = LocationFilter(show_country=False, data={"state": state.code.lower()})
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_other_country__field_error_reported(country, state):
    form = LocationFilter(
        show_country=True, data={"country": country.code[::-1], "state": state.code}
    )
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_valid_code__filter_is_defined(state):
    form = LocationFilter(show_country=False, data={"state": state.code})
    form.is_valid()
    assert Q(state__code=state.code) == form.get_filters()


def test_county_field__with_valid_code__form_is_valid(county):
    form = LocationFilter(show_country=False, data={"county": county.code})
    assert form.is_valid()


def test_county_field__with_invalid_code__form_is_invalid(county):
    form = LocationFilter(show_country=False, data={"county": county.code[::-1]})
    assert not form.is_valid()


def test_county_field__with_invalid_code__field_error_reported(county):
    form = LocationFilter(show_country=False, data={"county": county.code[::-1]})
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_lowercase_code__field_error_reported(county):
    form = LocationFilter(show_country=False, data={"county": county.code.lower()})
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_country__field_error_reported(country, county):
    form = LocationFilter(
        show_country=True, data={"country": country.code[::-1], "county": county.code}
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_state__field_error_reported(state, county):
    form = LocationFilter(
        show_country=False, data={"state": state.code[::-1], "county": county.code}
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_valid_code__filter_is_defined(county):
    form = LocationFilter(show_country=False, data={"county": county.code})
    form.is_valid()
    assert Q(county__code=county.code) == form.get_filters()


def test_location_field__with_valid_code__form_is_valid(location):
    form = LocationFilter(show_country=False, data={"location": location.identifier})
    assert form.is_valid()


def test_location_field__with_invalid_code__form_is_invalid(location):
    form = LocationFilter(
        show_country=False, data={"location": location.identifier[::-1]}
    )
    assert not form.is_valid()


def test_location_field__with_invalid_code__field_error_reported(location):
    form = LocationFilter(
        show_country=False, data={"location": location.identifier[::-1]}
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_lowercase_code__field_error_reported(location):
    form = LocationFilter(
        show_country=False, data={"location": location.identifier.lower()}
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_country__field_error_reported(country, location):
    form = LocationFilter(
        show_country=True,
        data={"country": country.code[::-1], "location": location.identifier},
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_state__field_error_reported(state, location):
    form = LocationFilter(
        show_country=False,
        data={"state": state.code[::-1], "location": location.identifier},
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_county__field_error_reported(county, location):
    form = LocationFilter(
        show_country=False,
        data={"country": county.code[::-1], "location": location.identifier},
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_valid_code__filter_is_defined(location):
    form = LocationFilter(show_country=False, data={"location": location.identifier})
    form.is_valid()
    assert Q(location__identifier=location.identifier) == form.get_filters()


def test_observer_field__with_valid_code__form_is_valid(observer):
    form = ObserverFilter(data={"observer": observer.identifier})
    assert form.is_valid()


def test_observer_field__with_invalid_code__form_is_invalid(observer):
    form = ObserverFilter(
        data={"observer": observer.identifier[::-1]}
    )
    assert not form.is_valid()


def test_observer_field__with_invalid_code__field_error_reported(observer):
    form = ObserverFilter(
        data={"observer": observer.identifier[::-1]}
    )
    form.is_valid()
    assert "observer" in form.errors


def test_observer_field__with_lowercase_code__field_error_reported(observer):
    form = ObserverFilter(
        data={"observer": observer.identifier.lower()}
    )
    form.is_valid()
    assert "observer" in form.errors


def test_observer_field__with_valid_code__filter_is_defined(observer):
    form = ObserverFilter(data={"observer": observer.identifier})
    form.is_valid()
    assert Q(observer__identifier=observer.identifier) == form.get_filters()


def test_start_field__invalid_date__field_error_reported(db_no_rollback):
    form = DateRangeFilter(data={"start": "2025-01"})
    form.is_valid()
    assert "start" in form.errors


def test_start_field__after_finish_date__field_error_reported(db_no_rollback):
    form = DateRangeFilter(
        data={"start": "2025-01-02", "finish": "2025-01-01"}
    )
    form.is_valid()
    assert "start" in form.errors


def test_start_field__with_valid_date__filter_is_defined(db_no_rollback, last_week):
    form = DateRangeFilter(data={"start": last_week})
    form.is_valid()
    assert Q(date__gte=last_week) == form.get_filters()


def test_finish_field__invalid_date__field_error_reported(db_no_rollback):
    form = DateRangeFilter(data={"finish": "2025-01"})
    form.is_valid()
    assert "finish" in form.errors


def test_finish_field__with_valid_date__filter_is_defined(db_no_rollback, last_week):
    form = DateRangeFilter(data={"finish": last_week})
    form.is_valid()
    assert Q(date__lte=last_week) == form.get_filters()


def test_hotspot_field__invalid_boolean__field_error_reported(db_no_rollback):
    form = HotspotFilter(data={"hotspot": "Tru"})
    form.is_valid()
    assert "hotspot" in form.errors


def test_hotspot_field__with_valid_data__filter_is_defined(db_no_rollback):
    form = HotspotFilter(data={"hotspot": True})
    form.is_valid()
    assert Q(location__hotspot="True") == form.get_filters()


def test_category_field__invalid_choice__field_error_reported(db_no_rollback):
    form = CategoryFilter(data={"category": "spuh"})
    form.is_valid()
    assert "category" in form.errors


def test_category_field__with_valid_data__filter_is_defined(db_no_rollback):
    form = CategoryFilter(data={"category": "species"})
    form.is_valid()
    assert Q(species__category="species") == form.get_filters()


def test_checklist_order_field__default_order(db_no_rollback):
    form = ChecklistOrder(data={})
    form.is_valid()
    assert "-started" in form.get_ordering()


def test_checklist_order_field__ordering_set(db_no_rollback):
    form = ChecklistOrder(data={"order": "-species_count"})
    form.is_valid()
    assert "-species_count" in form.get_ordering()


def test_checklist_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = ChecklistOrder(data={"order": "-species_coun"})
    form.is_valid()
    assert "order" in form.errors


def test_observation_order_field__default_order(db_no_rollback):
    form = ObservationOrder(data={})
    form.is_valid()
    assert "-started" in form.get_ordering()


def test_observation_order_field__ordering_set(db_no_rollback):
    form = ObservationOrder(data={"order": "-count"})
    form.is_valid()
    assert "-count" in form.get_ordering()


def test_observation_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = ObservationOrder(data={"order": "-coun"})
    form.is_valid()
    assert "order" in form.errors


def test_seen_order_field__default_order(db_no_rollback):
    form = SeenOrder(data={})
    form.is_valid()
    assert ("species", "date") == form.get_ordering()


def test_seen_order_field__ordering_set(db_no_rollback):
    form = SeenOrder(data={"order": "-seen"})
    form.is_valid()
    assert ("species", "-date") == form.get_ordering()


def test_seen_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = SeenOrder(data={"order": "-see"})
    form.is_valid()
    assert "order" in form.errors
