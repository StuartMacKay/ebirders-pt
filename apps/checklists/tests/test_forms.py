from checklists.filters import ChecklistFilter


def test_country_field__with_valid_code__form_is_valid(country):
    filterset = ChecklistFilter(show_country=True, data={"country": country.code})
    filterset.is_valid()
    assert filterset.form.is_valid()


def test_country_field__with_invalid_code__form_is_invalid(country):
    filterset = ChecklistFilter(show_country=True, data={"country": country.code[::-1]})
    filterset.is_valid()
    assert not filterset.form.is_valid()


def test_country_field__with_invalid_code__field_error_reported(country):
    filterset = ChecklistFilter(show_country=True, data={"country": country.code[::-1]})
    filterset.is_valid()
    assert "country" in filterset.form.errors


def test_country_field__with_lowercase_code__field_error_reported(country):
    filterset = ChecklistFilter(
        show_country=True, data={"country": country.code.lower()}
    )
    filterset.is_valid()
    assert "country" in filterset.form.errors


def test_country_field__with_short_code__field_error_reported(country):
    filterset = ChecklistFilter(show_country=True, data={"country": country.code[:-1]})
    filterset.is_valid()
    assert "country" in filterset.form.errors


def test_country_field__with_long_code__field_error_reported(country):
    filterset = ChecklistFilter(show_country=True, data={"country": country.code + "X"})
    filterset.is_valid()
    assert "country" in filterset.form.errors


def test_state_field__with_valid_code__form_is_valid(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code})
    filterset.is_valid()
    assert filterset.form.is_valid()


def test_state_field__with_invalid_code__form_is_invalid(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code[::-1]})
    filterset.is_valid()
    assert not filterset.form.is_valid()


def test_state_field__with_invalid_code__field_error_reported(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code[::-1]})
    filterset.is_valid()
    assert "state" in filterset.form.errors


def test_state_field__with_lowercase_code__field_error_reported(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code.lower()})
    filterset.is_valid()
    assert "state" in filterset.form.errors


def test_state_field__with_short_code__field_error_reported(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code[:-1]})
    filterset.is_valid()
    assert "state" in filterset.form.errors


def test_state_field__with_long_code__field_error_reported(state):
    filterset = ChecklistFilter(show_country=False, data={"state": state.code + "X"})
    filterset.is_valid()
    assert "state" in filterset.form.errors


def test_county_field__with_valid_code__form_is_valid(county):
    filterset = ChecklistFilter(show_country=False, data={"county": county.code})
    filterset.is_valid()
    assert filterset.form.is_valid()


def test_county_field__with_invalid_code__form_is_invalid(county):
    filterset = ChecklistFilter(show_country=False, data={"county": county.code[::-1]})
    filterset.is_valid()
    assert not filterset.form.is_valid()


def test_county_field__with_invalid_code__field_error_reported(county):
    filterset = ChecklistFilter(show_country=False, data={"county": county.code[::-1]})
    filterset.is_valid()
    assert "county" in filterset.form.errors


def test_county_field__with_lowercase_code__field_error_reported(county):
    filterset = ChecklistFilter(
        show_country=False, data={"county": county.code.lower()}
    )
    filterset.is_valid()
    assert "county" in filterset.form.errors


def test_county_field__with_short_code__field_error_reported(county):
    filterset = ChecklistFilter(show_country=False, data={"county": county.code[:-1]})
    filterset.is_valid()
    assert "county" in filterset.form.errors


def test_county_field__with_long_code__field_error_reported(county):
    filterset = ChecklistFilter(show_country=False, data={"county": county.code + "X"})
    filterset.is_valid()
    assert "county" in filterset.form.errors


def test_location_field__with_valid_code__form_is_valid(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier}
    )
    filterset.is_valid()
    assert filterset.form.is_valid()


def test_location_field__with_invalid_code__form_is_invalid(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier[::-1]}
    )
    filterset.is_valid()
    assert not filterset.form.is_valid()


def test_location_field__with_invalid_code__field_error_reported(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier[::-1]}
    )
    filterset.is_valid()
    assert "location" in filterset.form.errors


def test_location_field__with_lowercase_code__field_error_reported(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier.lower()}
    )
    filterset.is_valid()
    assert "location" in filterset.form.errors


def test_location_field__with_short_code__field_error_reported(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier[:-1]}
    )
    filterset.is_valid()
    assert "location" in filterset.form.errors


def test_location_field__with_long_code__field_error_reported(location):
    filterset = ChecklistFilter(
        show_country=False, data={"location": location.identifier + "X"}
    )
    filterset.is_valid()
    assert "location" in filterset.form.errors


def test_observer_field__with_valid_code__form_is_valid(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier}
    )
    filterset.is_valid()
    assert filterset.form.is_valid()


def test_observer_field__with_invalid_code__form_is_invalid(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier[::-1]}
    )
    filterset.is_valid()
    assert not filterset.form.is_valid()


def test_observer_field__with_invalid_code__field_error_reported(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier[::-1]}
    )
    filterset.is_valid()
    assert "observer" in filterset.form.errors


def test_observer_field__with_lowercase_code__field_error_reported(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier.lower()}
    )
    filterset.is_valid()
    assert "observer" in filterset.form.errors


def test_observer_field__with_short_code__field_error_reported(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier[:-1]}
    )
    filterset.is_valid()
    assert "observer" in filterset.form.errors


def test_observer_field__with_long_code__field_error_reported(observer):
    filterset = ChecklistFilter(
        show_country=False, data={"observer": observer.identifier + "X"}
    )
    filterset.is_valid()
    assert "observer" in filterset.form.errors


def test_start_field__invalid_date__field_error_reported():
    filterset = ChecklistFilter(
        show_country=False, data={"start": "2025-01"}
    )
    filterset.is_valid()
    assert "start" in filterset.form.errors


def test_start_field__after_finish_date__field_error_reported():
    filterset = ChecklistFilter(
        show_country=False, data={"start": "2025-01-02", "finish": "2025-01-01"}
    )
    filterset.is_valid()
    assert "start" in filterset.form.errors


def test_finish_field__invalid_date__field_error_reported():
    filterset = ChecklistFilter(
        show_country=False, data={"finish": "2025-01"}
    )
    filterset.is_valid()
    assert "finish" in filterset.form.errors


def test_hotspot_field__invalid_boolean__field_error_reported():
    filterset = ChecklistFilter(
        show_country=False, data={"hotspot": "Tru"}
    )
    filterset.is_valid()
    assert "hotspot" in filterset.form.errors


def test_order_field__invalid_order__field_error_reported():
    filterset = ChecklistFilter(
        show_country=False, data={"order": "-species_coun"}
    )
    filterset.is_valid()
    assert "order" in filterset.form.errors
