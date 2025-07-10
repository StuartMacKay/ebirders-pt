import json

from django.urls import reverse

from ebird.api.data.models import Country, County, Location, Observer, Species, State


def test_data_autocomplete__returns_countries(db_no_rollback, client):
    url = reverse("filters:countries")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for country in Country.objects.all():
        assert table.get(country.code)


def test_data_autocomplete__returns_states(db_no_rollback, client):
    url = reverse("filters:states")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for state in State.objects.all():
        assert table.get(state.code)


def test_data_autocomplete__returns_counties(db_no_rollback, client):
    url = reverse("filters:counties")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for county in County.objects.all():
        assert table.get(county.code)


def test_data_autocomplete__returns_locations(db_no_rollback, client):
    url = reverse("filters:locations")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for location in Location.objects.all():
        assert table.get(location.identifier)


def test_data_autocomplete__returns_observers(db_no_rollback, client):
    url = reverse("filters:observers")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for observer in Observer.objects.all():
        assert table.get(observer.identifier)


def test_data_autocomplete__returns_common_names(db_no_rollback, client):
    url = reverse("filters:common-name")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for species in Species.objects.all():
        assert table.get(species.species_code)


def test_data_autocomplete__returns_scientifc_names(db_no_rollback, client):
    url = reverse("filters:scientific-name")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for species in Species.objects.all():
        assert table.get(species.species_code)
