from filters.forms import CategoryFilter


def test_category_queryset_expr():
    assert CategoryFilter.filters["category"] == "species__category"


def test_no_ordering():
    assert CategoryFilter().get_ordering() == []
