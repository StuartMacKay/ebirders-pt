from filters.forms import LocationFilter


def test_country_queryset_expr():
    assert LocationFilter.filters["country"] == "country__code"

def test_state_queryset_expr():
    assert LocationFilter.filters["state"] == "state__code__in"

def test_county_queryset_expr():
    assert LocationFilter.filters["county"] == "county__code__in"

def test_location_queryset_expr():
    assert LocationFilter.filters["location"] == "location__identifier__in"

def test_hotspot_queryset_expr():
    assert LocationFilter.filters["hotspot"] == "location__hotspot"

def test_no_ordering():
    assert LocationFilter(show_country=True).get_ordering() == []
