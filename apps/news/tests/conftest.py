import random
import re

from django.utils.http import urlencode

from ebird.api.data.models import Country, County, State

import pytest


@pytest.fixture
def search_by_country():
    country = random.choice(Country.objects.all()[:])
    return urlencode({"code": country.code, "search": country.place})


@pytest.fixture
def search_by_state():
    state = random.choice(State.objects.all()[:])
    if Country.objects.count() == 1:
        country = Country.objects.get().name
        place = re.sub(", %s$" % country, "", state.place)
    else:
        place = state.place
    return urlencode({"code": state.code, "search": place})


@pytest.fixture
def search_by_county():
    county = random.choice(County.objects.all()[:])
    if Country.objects.count() == 1:
        country = Country.objects.get().name
        place = re.sub(", %s$" % country, "", county.place)
    else:
        place = county.place
    return urlencode({"code": county.code, "search": place})
