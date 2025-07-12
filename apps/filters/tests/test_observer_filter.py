from filters.forms import ObserverFilter


def test_observer_queryset_expr():
    assert ObserverFilter.filters["observer"] == "observer__identifier"


def test_no_ordering():
    assert ObserverFilter().get_ordering() == []
