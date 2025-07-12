from django.http import QueryDict

from filters.forms import ObservationOrder


def test_no_filters():
    assert ObservationOrder.filters == {}


def test_default_ordering():
    form = ObservationOrder(data=QueryDict())
    assert form.is_valid()
    assert form.get_ordering() == ('-started',)
