from django.http import QueryDict

from filters.forms import ChecklistOrder


def test_no_filters():
    assert ChecklistOrder.filters == {}


def test_default_ordering():
    form = ChecklistOrder(data=QueryDict())
    assert form.is_valid()
    assert form.get_ordering() == ('-started',)
