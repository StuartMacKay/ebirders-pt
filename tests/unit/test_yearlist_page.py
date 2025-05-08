import datetime as dt

from django.urls import reverse

import pytest


@pytest.fixture
def year():
    return dt.date.today().year


@pytest.fixture
def url(year):
    return reverse("species:yearlist", kwargs={"year": year})


def test_yearlist_page__displayed(db_no_rollback, client, url):
    response = client.get(url)
    assert response.status_code == 200
