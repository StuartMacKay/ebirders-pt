from data.forms import (
    CategoryFilter,
    DateRangeFilter,
    LocationFilter,
    ObserverFilter,
    SeenOrder,
)
from species.forms import SpeciesFilterForm


def test_species_filter_form__inherits_from__location_filter(db_no_rollback):
    isinstance(SpeciesFilterForm(show_country=False), LocationFilter)


def test_species_filter_form__inherits_from__observer_filter(db_no_rollback):
    isinstance(SpeciesFilterForm(show_country=False), ObserverFilter)


def test_species_filter_form__inherits_from__date_range_filter(db_no_rollback):
    isinstance(SpeciesFilterForm(show_country=False), DateRangeFilter)


def test_species_filter_form__inherits_from__species_filter(db_no_rollback):
    isinstance(SpeciesFilterForm(show_country=False), CategoryFilter)


def test_species_filter_form__inherits_from__checklist_order(db_no_rollback):
    isinstance(SpeciesFilterForm(show_country=False), SeenOrder)
