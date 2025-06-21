from django.urls import reverse


def test_list_view__is_paginated(db_no_rollback, client):
    url = reverse("observations:list")
    response = client.get(url)
    view = response.context["view"]
    assert view.paginate_by is not None


def test_list_view__filter_by_country(db_no_rollback, client, country):
    url = reverse("observations:list")
    response = client.get(url, data={"country": country.code})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.country == country


def test_list_view__filter_by_state(db_no_rollback, client, state):
    url = reverse("observations:list")
    response = client.get(url, data={"state": state.code})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.state == state


def test_list_view__filter_by_county(db_no_rollback, client, county):
    url = reverse("observations:list")
    response = client.get(url, data={"county": county.code})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.county == county


def test_list_view__filter_by_location(db_no_rollback, client, location):
    url = reverse("observations:list")
    response = client.get(url, data={"location": location.identifier})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.location == location


def test_list_view__filter_by_observer(db_no_rollback, client, observer):
    url = reverse("observations:list")
    response = client.get(url, data={"observer": observer.identifier})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.observer == observer


def test_list_view__filter_by_species(db_no_rollback, client, species):
    url = reverse("observations:list")
    response = client.get(url, data={"species": species.species_code})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.species == species


def test_list_view__filter_by_start(db_no_rollback, client, last_week):
    url = reverse("observations:list")
    response = client.get(url, data={"start": last_week})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.date >= last_week


def test_list_view__filter_by_finish(db_no_rollback, client, last_week):
    url = reverse("observations:list")
    response = client.get(url, data={"finish": last_week})
    objects = response.context["object_list"]
    assert objects.count() != 0
    for obj in objects:
        assert obj.date <= last_week
