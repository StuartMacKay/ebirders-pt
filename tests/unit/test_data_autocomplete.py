import json

from django.urls import reverse

from data.models import Country, County, Location, Observer, Species, State


def test_data_autocomplete__returns_countries(db_no_rollback, client):
    url = reverse("data:countries")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for country in Country.objects.all():
        assert table.get(country.code)


def test_data_autocomplete__returns_states(db_no_rollback, client):
    url = reverse("data:states")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for state in State.objects.all():
        assert table.get(state.code)


def test_data_autocomplete__returns_counties(db_no_rollback, client):
    url = reverse("data:counties")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for county in County.objects.all():
        assert table.get(county.code)


def test_data_autocomplete__returns_locations(db_no_rollback, client):
    url = reverse("data:locations")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for location in Location.objects.all():
        assert table.get(location.identifier)


def test_data_autocomplete__returns_observers(db_no_rollback, client):
    url = reverse("data:observers")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for observer in Observer.objects.all():
        assert table.get(observer.identifier)


def test_data_autocomplete__returns_species(db_no_rollback, client):
    url = reverse("data:species")
    response = client.get(url)
    data = json.loads(response.content)
    table = {item["id"]: item["text"] for item in data["results"]}
    for species in Species.objects.all():
        assert table.get(species.species_code)
