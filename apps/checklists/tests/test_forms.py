from checklists.forms import (
    ChecklistFilterForm,
    ChecklistOrder,
    DateRangeFilter,
    HotspotFilter,
    LocationFilter,
    ObserverFilter,
)


def test_checklist_filter_form__inherits_from__location_filter(db_no_rollback):
        isinstance(ChecklistFilterForm(show_country=False), LocationFilter)


def test_checklist_filter_form__inherits_from__observer_filter(db_no_rollback):
        isinstance(ChecklistFilterForm(show_country=False), ObserverFilter)


def test_checklist_filter_form__inherits_from__date_range_filter(db_no_rollback):
        isinstance(ChecklistFilterForm(show_country=False), DateRangeFilter)


def test_checklist_filter_form__inherits_from__hotspot_filter(db_no_rollback):
        isinstance(ChecklistFilterForm(show_country=False), HotspotFilter)


def test_checklist_filter_form__inherits_from__checklist_order(db_no_rollback):
        isinstance(ChecklistFilterForm(show_country=False), ChecklistOrder)
