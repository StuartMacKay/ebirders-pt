from filters.forms import DateRangeFilter


def test_start_queryset_expr():
    assert DateRangeFilter.filters["start"] == "date__gte"


def test_finish_queryset_expr():
    assert DateRangeFilter.filters["finish"] == "date__lte"


def test_no_ordering():
    assert DateRangeFilter().get_ordering() == []
