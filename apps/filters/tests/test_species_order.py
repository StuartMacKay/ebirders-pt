from django.http import QueryDict

from filters.forms import SpeciesOrder


def test_no_filters():
    assert SpeciesOrder.filters == {}


def test_default_ordering():
    # Return the list in taxonomic order with first observation
    form = SpeciesOrder(data=QueryDict())
    assert form.is_valid()
    assert form.get_ordering() == ("species", "started")
