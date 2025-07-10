import json
import re

from django.urls import reverse

from ebird.api.data.models import Country, County, State

import pytest


@pytest.fixture
def url():
    return reverse("news:autocomplete")


@pytest.fixture
def table(db_no_rollback, client, url):
    response = client.get(url)
    data = json.loads(response.content)
    return {item["value"]: item["label"] for item in data}


def test_news_autocomplete__returns_data(db_no_rollback, client, url):
    response = client.get(url)
    json.loads(response.content)


def test_news_autocomplete__returns_states(table):
    for state in State.objects.all():
        assert table.get(state.code)


def test_news_autocomplete__country_trimmed_from_state(table):
    if Country.objects.count() != 1:
        return
    country = Country.objects.get().name
    for state in State.objects.all():
        place = re.sub(r", %s$" % country, "", state.place)
        assert table[state.code] == place


def test_news_autocomplete__returns_counties(table):
    for county in County.objects.all():
        assert table.get(county.code)


def test_news_autocomplete__country_trimmed_from_county(table):
    if Country.objects.count() != 1:
        return
    country = Country.objects.get().name
    for county in County.objects.all():
        place = re.sub(r", %s$" % country, "", county.place)
        assert table[county.code] == place
