import datetime as dt

from django.urls import reverse

from tests.factories import ObserverFactory

import pytest


@pytest.fixture
def observer():
    return ObserverFactory.create().identifier


@pytest.fixture
def today():
    return dt.date.today()


@pytest.fixture
def url(observer, today):
    return "%s?observer=%s&date=%s" % (reverse("observations:big-day"), observer, today)


def test_big_day_page__displayed(db_no_rollback, client, url):
    response = client.get(url)
    assert response.status_code == 200
