from checklists.filters import ChecklistFilter
from checklists.forms import ChecklistFilterForm


def test_form():
    filterset = ChecklistFilter(show_country=False)
    assert isinstance(filterset.form, ChecklistFilterForm)


def test_by_country__filter_is_valid(country):
    filterset = ChecklistFilter(show_country=True, data={"country": country.code})
    assert filterset.is_valid()


def test_by_country__queryset_returned(country):
    filterset = ChecklistFilter(show_country=True, data={"country": country.code})
    assert filterset.qs.exists()


def test_by_state__filter_is_valid(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code})
    assert filterset.is_valid()


def test_by_state_queryset_returned(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code})
    assert filterset.qs.exists()


def test_by_county__filter_is_valid(county):
    filterset = ChecklistFilter(show_country=False, data={"county": county.code})
    assert filterset.is_valid()


def test_by_county__queryset_returned(county):
    filterset = ChecklistFilter(show_country=False, data={"county": county.code})
    assert filterset.qs.exists()


def test_by_location__filter_is_valid(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier}
    )
    assert filterset.is_valid()


def test_by_location__queryset_returned(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier}
    )
    assert filterset.qs.exists()


def test_by_observer__filter_is_valid(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier}
    )
    assert filterset.is_valid()


def test_by_observer__queryset_returned(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier}
    )
    assert filterset.qs.exists()


def test_by_from__filter_is_valid(db_no_rollback, last_week):
    filterset = ChecklistFilter(show_country=False, data={"from": last_week})
    assert filterset.is_valid()


def test_by_from_queryset_returned(db_no_rollback, last_week):
    filterset = ChecklistFilter(show_country=False, data={"from": last_week})
    assert filterset.qs.exists()


def test_by_until__filter_is_valid(db_no_rollback, last_week):
    filterset = ChecklistFilter(show_country=False, data={"until": last_week})
    assert filterset.is_valid()


def test_by_until_queryset_returned(db_no_rollback, last_week):
    filterset = ChecklistFilter(show_country=False, data={"until": last_week})
    assert filterset.qs.exists()


def test_by_hotspot__filter_is_valid(db_no_rollback):
    filterset = ChecklistFilter(show_country=False, data={"hotspot": "True"})
    assert filterset.is_valid()


def test_by_hotspot_queryset_returned(db_no_rollback):
    filterset = ChecklistFilter(show_country=False, data={"hotspot": "True"})
    assert filterset.qs.exists()


def test_by_species_count_order__filter_is_valid(db_no_rollback):
    filterset = ChecklistFilter(show_country=False, data={"order": "species_count"})
    assert filterset.is_valid()


def test_by_species_count_queryset_returned(db_no_rollback):
    filterset = ChecklistFilter(show_country=False, data={"order": "species_count"})
    assert filterset.qs.exists()
