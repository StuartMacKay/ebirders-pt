from django.urls import reverse

import pytest


@pytest.fixture
def url():
    return reverse("news:latest")


def test_latest_news_page(db_no_rollback, client, url):  # noqa
    response = client.get(url)
    assert response.status_code == 200


def test_latest_news_page__search_by_country(
    db_no_rollback, client, url, search_by_country
):
    response = client.get("%s?%s" % (url, search_by_country))
    assert response.status_code == 200


def test_latest_news_page__search_by_state(
    db_no_rollback, client, url, search_by_state
):
    response = client.get("%s?%s" % (url, search_by_state))
    assert response.status_code == 200


def test_latest_news_page__search_by_county(
    db_no_rollback, client, url, search_by_county
):
    response = client.get("%s?%s" % (url, search_by_county))
    assert response.status_code == 200
