from checklists.forms import ChecklistFilterForm


def test_country_field__with_valid_code__form_is_valid(country):
    form = ChecklistFilterForm(show_country=True, data={"country": country.code})
    assert form.is_valid()


def test_country_field__with_invalid_code__form_is_invalid(country):
    form = ChecklistFilterForm(show_country=True, data={"country": country.code[::-1]})
    assert not form.is_valid()


def test_country_field__with_invalid_code__field_error_reported(country):
    form = ChecklistFilterForm(show_country=True, data={"country": country.code[::-1]})
    form.is_valid()
    assert "country" in form.errors


def test_country_field__with_lowercase_code__field_error_reported(country):
    form = ChecklistFilterForm(show_country=True, data={"country": country.code.lower()})
    form.is_valid()
    assert "country" in form.errors


def test_state_field__with_valid_code__form_is_valid(state):
    form = ChecklistFilterForm(show_country=False, data={"state": state.code})
    assert form.is_valid()


def test_state_field__with_invalid_code__form_is_invalid(state):
    form = ChecklistFilterForm(show_country=False, data={"state": state.code[::-1]})
    assert not form.is_valid()


def test_state_field__with_invalid_code__field_error_reported(state):
    form = ChecklistFilterForm(show_country=False, data={"state": state.code[::-1]})
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_lowercase_code__field_error_reported(state):
    form = ChecklistFilterForm(show_country=False, data={"state": state.code.lower()})
    form.is_valid()
    assert "state" in form.errors


def test_state_field__with_other_country__field_error_reported(country, state):
    form = ChecklistFilterForm(
        show_country=True, data={"country": country.code[::-1], "state": state.code}
    )
    form.is_valid()
    assert "state" in form.errors


def test_county_field__with_valid_code__form_is_valid(county):
    form = ChecklistFilterForm(show_country=False, data={"county": county.code})
    assert form.is_valid()


def test_county_field__with_invalid_code__form_is_invalid(county):
    form = ChecklistFilterForm(show_country=False, data={"county": county.code[::-1]})
    assert not form.is_valid()


def test_county_field__with_invalid_code__field_error_reported(county):
    form = ChecklistFilterForm(show_country=False, data={"county": county.code[::-1]})
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_lowercase_code__field_error_reported(county):
    form = ChecklistFilterForm(show_country=False, data={"county": county.code.lower()})
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_country__field_error_reported(country, county):
    form = ChecklistFilterForm(
        show_country=True, data={"country": country.code[::-1], "county": county.code}
    )
    form.is_valid()
    assert "county" in form.errors


def test_county_field__with_other_state__field_error_reported(state, county):
    form = ChecklistFilterForm(
        show_country=False, data={"state": state.code[::-1], "county": county.code}
    )
    form.is_valid()
    assert "county" in form.errors


def test_location_field__with_valid_code__form_is_valid(location):
    form = ChecklistFilterForm(show_country=False, data={"location": location.identifier})
    assert form.is_valid()


def test_location_field__with_invalid_code__form_is_invalid(location):
    form = ChecklistFilterForm(show_country=False, data={"location": location.identifier[::-1]})
    assert not form.is_valid()


def test_location_field__with_invalid_code__field_error_reported(location):
    form = ChecklistFilterForm(show_country=False, data={"location": location.identifier[::-1]})
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_lowercase_code__field_error_reported(location):
    form = ChecklistFilterForm(
        show_country=False, data={"location": location.identifier.lower()}
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_country__field_error_reported(country, location):
    form = ChecklistFilterForm(
        show_country=True, data={"country": country.code[::-1], "location": location.identifier}
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_state__field_error_reported(state, location):
    form = ChecklistFilterForm(
        show_country=False, data={"state": state.code[::-1], "location": location.identifier}
    )
    form.is_valid()
    assert "location" in form.errors


def test_location_field__with_other_county__field_error_reported(county, location):
    form = ChecklistFilterForm(
        show_country=False, data={"country": county.code[::-1], "location": location.identifier}
    )
    form.is_valid()
    assert "location" in form.errors


def test_observer_field__with_valid_code__form_is_valid(observer):
    form = ChecklistFilterForm(show_country=False, data={"observer": observer.identifier})
    assert form.is_valid()


def test_observer_field__with_invalid_code__form_is_invalid(observer):
    form = ChecklistFilterForm(show_country=False, data={"observer": observer.identifier[::-1]})
    assert not form.is_valid()


def test_observer_field__with_invalid_code__field_error_reported(observer):
    form = ChecklistFilterForm(show_country=False, data={"observer": observer.identifier[::-1]})
    form.is_valid()
    assert "observer" in form.errors


def test_observer_field__with_lowercase_code__field_error_reported(observer):
    form = ChecklistFilterForm(
        show_country=False, data={"observer": observer.identifier.lower()}
    )
    form.is_valid()
    assert "observer" in form.errors


def test_start_field__invalid_date__field_error_reported(db_no_rollback):
    form = ChecklistFilterForm(show_country=False, data={"start": "2025-01"})
    form.is_valid()
    assert "start" in form.errors


def test_start_field__after_finish_date__field_error_reported(db_no_rollback):
    form = ChecklistFilterForm(
        show_country=False, data={"start": "2025-01-02", "finish": "2025-01-01"}
    )
    form.is_valid()
    assert "start" in form.errors


def test_finish_field__invalid_date__field_error_reported(db_no_rollback):
    form = ChecklistFilterForm(show_country=False, data={"finish": "2025-01"})
    form.is_valid()
    assert "finish" in form.errors


def test_hotspot_field__invalid_boolean__field_error_reported(db_no_rollback):
    form = ChecklistFilterForm(show_country=False, data={"hotspot": "Tru"})
    form.is_valid()
    assert "hotspot" in form.errors


def test_order_field__invalid_order__field_error_reported(db_no_rollback):
    form = ChecklistFilterForm(show_country=False, data={"order": "-species_coun"})
    form.is_valid()
    assert "order" in form.errors
