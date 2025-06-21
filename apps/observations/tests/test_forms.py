from data.forms import (
    DateRangeFilter,
    LocationFilter,
    ObservationOrder,
    ObserverFilter,
    SpeciesFilter,
)
from observations.forms import ObservationFilterForm


def test_checklist_filter_form__inherits_from__location_filter(db_no_rollback):
    isinstance(ObservationFilterForm(show_country=False), LocationFilter)


def test_checklist_filter_form__inherits_from__observer_filter(db_no_rollback):
    isinstance(ObservationFilterForm(show_country=False), ObserverFilter)


def test_checklist_filter_form__inherits_from__date_range_filter(db_no_rollback):
    isinstance(ObservationFilterForm(show_country=False), DateRangeFilter)


def test_checklist_filter_form__inherits_from__species_filter(db_no_rollback):
    isinstance(ObservationFilterForm(show_country=False), SpeciesFilter)


def test_checklist_filter_form__inherits_from__checklist_order(db_no_rollback):
    isinstance(ObservationFilterForm(show_country=False), ObservationOrder)
