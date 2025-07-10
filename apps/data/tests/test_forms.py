from django.db.models import Q
from django.http import QueryDict

from data.forms import (
    CategoryFilter,
    ChecklistOrder,
    DateRangeFilter,
    LocationFilter,
    ObservationOrder,
    ObserverFilter,
    SpeciesOrder,
)


def test_country_field__with_valid_code__form_is_valid(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s" % country.code)
    )
    assert form.is_valid()


def test_country_field__with_invalid_code__form_is_invalid(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s" % country.code[::-1])
    )
    assert not (form.is_valid())


def test_country_field__with_invalid_code__field_error_reported(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s" % country.code[::-1])
    )
    form.is_valid()
    assert "country" in form.errors


def test_country_field__with_lowercase_code__field_error_reported(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s" % country.code.lower())
    )
    form.is_valid()
    assert "country" in form.errors


def test_country_field__with_valid_code__filter_is_defined(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s" % country.code)
    )
    form.is_valid()
    assert Q(country__code=country.code) == form.get_filters()


def test_state_field__with_valid_code__form_is_valid(state):
    form = LocationFilter(show_country=False, data=QueryDict("state=%s" % state.code))
    assert form.is_valid()


def test_state_field__with_invalid_code__form_is_invalid(state):
    form = LocationFilter(
        show_country=False, data=QueryDict("state=%s" % state.code[::-1])
    )
    assert not form.is_valid()


def test_state_field__with_invalid_code__field_error_reported(state):
    form = LocationFilter(
        show_country=False, data=QueryDict("state=%s" % state.code[::-1])
    )
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_lowercase_code__field_error_reported(state):
    form = LocationFilter(
        show_country=False, data=QueryDict("state=%s" % state.code.lower())
    )
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_other_country__field_error_reported(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s&state=AA" % country.code)
    )
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_valid_code__filter_is_defined(state):
    form = LocationFilter(show_country=False, data=QueryDict("state=%s" % state.code))
    form.is_valid()
    assert Q(state__code__in=[state.code]) == form.get_filters()


def test_county_field__with_valid_code__form_is_valid(county):
    form = LocationFilter(show_country=False, data=QueryDict("county=%s" % county.code))
    assert form.is_valid()


def test_county_field__with_invalid_code__form_is_invalid(county):
    form = LocationFilter(
        show_country=False, data=QueryDict("county=%s" % county.code[::-1])
    )
    assert not form.is_valid()


def test_county_field__with_invalid_code__field_error_reported(county):
    form = LocationFilter(
        show_country=False, data=QueryDict("county=%s" % county.code[::-1])
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_lowercase_code__field_error_reported(county):
    form = LocationFilter(
        show_country=False, data=QueryDict("county=%s" % county.code.lower())
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_country__field_error_reported(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s&county=AA" % country.code)
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_state__field_error_reported(state):
    form = LocationFilter(
        show_country=False, data=QueryDict("state=%s&county=AA" % state)
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_valid_code__filter_is_defined(county):
    form = LocationFilter(show_country=False, data=QueryDict("county=%s" % county.code))
    form.is_valid()
    assert Q(county__code__in=[county.code]) == form.get_filters()


def test_location_field__with_valid_code__form_is_valid(location):
    form = LocationFilter(
        show_country=False, data=QueryDict("location=%s" % location.identifier)
    )
    assert form.is_valid()


def test_location_field__with_invalid_code__form_is_invalid(location):
    form = LocationFilter(
        show_country=False, data=QueryDict("location=%s" % location.identifier[::-1])
    )
    assert not form.is_valid()


def test_location_field__with_invalid_code__field_error_reported(location):
    form = LocationFilter(
        show_country=False, data=QueryDict("location=%s" % location.identifier[::-1])
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_lowercase_code__field_error_reported(location):
    form = LocationFilter(
        show_country=False, data=QueryDict("location=%s" % location.identifier.lower())
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_country__field_error_reported(country):
    form = LocationFilter(
        show_country=True, data=QueryDict("country=%s&location=L00" % country.code)
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_state__field_error_reported(state, location):
    form = LocationFilter(
        show_country=False, data=QueryDict("state=%s&location=L00" % state.code)
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_county__field_error_reported(county, location):
    form = LocationFilter(
        show_country=False, data=QueryDict("county=%s&location=L00" % county.code)
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_valid_code__filter_is_defined(location):
    form = LocationFilter(
        show_country=False, data=QueryDict("location=%s" % location.identifier)
    )
    form.is_valid()
    assert Q(location__identifier__in=[location.identifier]) == form.get_filters()


def test_hotspot_field__with_valid_data__filter_is_defined(db_no_rollback):
    form = LocationFilter(show_country=False, data=QueryDict("hotspot=True"))
    form.is_valid()
    assert Q(location__hotspot="True") == form.get_filters()


def test_hotspot_field__invalid_boolean__field_error_reported(db_no_rollback):
    form = LocationFilter(show_country=False, data=QueryDict("hotspot=Tru"))
    assert "hotspot" in form.errors


def test_observer_field__with_valid_code__form_is_valid(observer):
    form = ObserverFilter(data=QueryDict("observer=%s" % observer.identifier))
    assert form.is_valid()


def test_observer_field__with_invalid_code__form_is_invalid(observer):
    form = ObserverFilter(data=QueryDict("observer=%s" % observer.identifier[::-1]))
    assert not form.is_valid()


def test_observer_field__with_invalid_code__field_error_reported(observer):
    form = ObserverFilter(data=QueryDict("observer=%s" % observer.identifier[::-1]))
    form.is_valid()
    assert "observer" in form.errors


def test_observer_field__with_lowercase_code__field_error_reported(observer):
    form = ObserverFilter(data=QueryDict("observer=%s" % observer.identifier.lower()))
    form.is_valid()
    assert "observer" in form.errors


def test_observer_field__with_valid_code__filter_is_defined(observer):
    form = ObserverFilter(data=QueryDict("observer=%s" % observer.identifier))
    form.is_valid()
    assert Q(observer__identifier=observer.identifier) == form.get_filters()


def test_start_field__invalid_date__field_error_reported(db_no_rollback):
    form = DateRangeFilter(data=QueryDict("start=%s" % "2025-01"))
    form.is_valid()
    assert "start" in form.errors


def test_start_field__after_finish_date__field_error_reported(db_no_rollback):
    form = DateRangeFilter(
        data=QueryDict("start=%s&finish=%s" % ("2025-01-02", "2025-01-01"))
    )
    form.is_valid()
    assert "start" in form.errors


def test_start_field__with_valid_date__filter_is_defined(db_no_rollback, last_week):
    form = DateRangeFilter(data=QueryDict("start=%s" % last_week))
    form.is_valid()
    assert Q(date__gte=last_week) == form.get_filters()


def test_finish_field__invalid_date__field_error_reported(db_no_rollback):
    form = DateRangeFilter(data=QueryDict("finish=%s" % "2025-01"))
    form.is_valid()
    assert "finish" in form.errors


def test_finish_field__with_valid_date__filter_is_defined(db_no_rollback, last_week):
    form = DateRangeFilter(data=QueryDict("finish=%s" % last_week))
    form.is_valid()
    assert Q(date__lte=last_week) == form.get_filters()


def test_category_field__invalid_choice__field_error_reported(db_no_rollback):
    form = CategoryFilter(data=QueryDict("category=spuh"))
    form.is_valid()
    assert "category" in form.errors


def test_category_field__with_valid_data__filter_is_defined(db_no_rollback):
    form = CategoryFilter(data=QueryDict("category=species"))
    form.is_valid()
    assert Q(species__category="species") == form.get_filters()


def test_checklist_order_field__default_order(db_no_rollback):
    form = ChecklistOrder(data=QueryDict(""))
    form.is_valid()
    assert "-started" in form.get_ordering()


def test_checklist_order_field__ordering_set(db_no_rollback):
    form = ChecklistOrder(data=QueryDict("order=%s" % "-species_count,-started"))
    form.is_valid()
    assert ["-species_count", "-started"] == form.get_ordering()


def test_checklist_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = ChecklistOrder(data=QueryDict("order=%s" % "-species_coun"))
    form.is_valid()
    assert "order" in form.errors


def test_observation_order_field__default_order(db_no_rollback):
    form = ObservationOrder(data=QueryDict(""))
    form.is_valid()
    assert "-started" in form.get_ordering()


def test_observation_order_field__ordering_set(db_no_rollback):
    form = ObservationOrder(data=QueryDict("order=%s" % "-count"))
    form.is_valid()
    assert "-count" in form.get_ordering()


def test_observation_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = ObservationOrder(data=QueryDict("order=%s" % "-coun"))
    form.is_valid()
    assert "order" in form.errors


def test_species_order_field__default_order(db_no_rollback):
    form = SpeciesOrder(data=QueryDict(""))
    form.is_valid()
    assert ("species", "started") == form.get_ordering()


def test_species_order_field__ordering_set(db_no_rollback):
    form = SpeciesOrder(data=QueryDict("order=%s" % "species,started"))
    form.is_valid()
    assert ["species", "started"] == form.get_ordering()


def test_species_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = SpeciesOrder(data=QueryDict("order=%s" % "species,-starte"))
    form.is_valid()
    assert "order" in form.errors
