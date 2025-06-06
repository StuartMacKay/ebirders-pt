import datetime as dt
import random
import re

from django.utils.http import urlencode

from dateutil.relativedelta import relativedelta

from data.models import Country, County, Location, Observer, Species, State

import pytest

# Test against a local database which has been populated with data from the
# eBird API, using the APILoader.
#
# This is by far the easiest and most effective option for several reasons:
#
# 1. It's real data.
# 2. It's easy to set up.
# 3. Does not require maintenance.
# 4. The data is not published, so there are no privacy issues.
# 5. You can easily test different eBird regions or languages.
# 6. You aan easily generate large datasets to test query performance.
# 7. Problems in production are going to show up locally too.
#
# Compared to fixture files, the data is always up to date, particularly if
# you run the APILoader in a cron job to download checklists daily.
#
# Compared to generated fixtures, the data is more accurate and comprehensive.
# Generating data with a similar profile, using tools like Factory Boy, would
# take a significant amount of effort. The code would also need to be maintained.


@pytest.fixture(scope="session")
def django_db_setup():
    # Don't create the database; don't run any migrations and don't tear
    # down the database when the tests are finished.
    pass


@pytest.fixture
def db_no_rollback(request, django_db_setup, django_db_blocker):
    # Use this instead of pytest.mark.django_db to access the database.
    django_db_blocker.unblock()
    yield
    django_db_blocker.restore()


# Query parameters for pages with a single search field


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


# Query parameters for pages with a set of filters


@pytest.fixture
def filter_by_country():
    country = random.choice(Country.objects.all()[:])
    return urlencode({"country": country.code})


@pytest.fixture
def filter_by_state():
    state = random.choice(State.objects.all()[:])
    return urlencode({"state": state.code})


@pytest.fixture
def filter_by_county():
    county = random.choice(County.objects.all()[:])
    return urlencode({"county": county.code})


@pytest.fixture
def filter_by_location():
    location = random.choice(Location.objects.all()[:])
    return urlencode({"location": location.identifier})


@pytest.fixture
def filter_by_observer():
    observer = random.choice(Observer.objects.all()[:])
    return urlencode({"observer": observer.identifier})


@pytest.fixture
def filter_by_start_date():
    date = dt.date.today() - relativedelta(days=30)
    return urlencode({"start": date.strftime("%Y-%m-%d")})


@pytest.fixture
def filter_by_end_date():
    date = dt.date.today() - relativedelta(days=30)
    return urlencode({"start": date.strftime("%Y-%m-%d")})


@pytest.fixture
def filter_by_date_range():
    finish = dt.date.today()
    start = finish - relativedelta(days=30)
    return urlencode(
        {"start": start.strftime("%Y-%m-%d"), "finish": finish.strftime("%Y-%m-%d")}
    )


@pytest.fixture
def filter_by_hotspot():
    choice = random.choice(["", "true", "false"])
    return urlencode({"hotspot": choice})


@pytest.fixture
def filter_by_species():
    species = random.choice(Species.objects.all()[:])
    return urlencode({"species": species.species_code})


@pytest.fixture
def ordered_by_species_count():
    choice = random.choice(["", "species_count", "-species_count"])
    return urlencode({"o": choice})


@pytest.fixture
def ordered_by_count():
    choice = random.choice(["", "count", "-count"])
    return urlencode({"o": choice})
