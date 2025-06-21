import datetime as dt
import random

from dateutil.relativedelta import MO, relativedelta

from data.models import Checklist, Country, County, Location, Observer, Species, State

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


@pytest.fixture
def country(db_no_rollback):
    return random.choice(list(Country.objects.all()))


@pytest.fixture
def state(db_no_rollback):
    return random.choice(list(State.objects.all()))


@pytest.fixture
def county(db_no_rollback):
    return random.choice(list(County.objects.all()))


@pytest.fixture
def location(db_no_rollback):
    return random.choice(list(Location.objects.all()))


@pytest.fixture
def observer(db_no_rollback):
    return random.choice(list(Observer.objects.all()))


@pytest.fixture
def species(db_no_rollback):
    return random.choice(list(Species.objects.all()))


@pytest.fixture
def category(db_no_rollback):
    return random.choice(["species", "issf", "domestic", "hybrid"])


@pytest.fixture
def checklist(db_no_rollback):
    return random.choice(list(Checklist.objects.all()))


@pytest.fixture
def last_week():
    return dt.date.today() - relativedelta(weekday=MO(-2))
