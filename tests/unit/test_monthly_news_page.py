import datetime as dt

from django.urls import reverse

import pytest


@pytest.fixture
def latest_month():
    return reverse("news:monthly")


@pytest.fixture
def selected_month():
    today = dt.date.today()
    return reverse("news:for-month", kwargs={"year": today.year, "month": today.month})


def test_monthly_news_page__latest_month(  # noqa
    db_no_rollback, client, latest_month
):
    response = client.get(latest_month)
    assert response.status_code == 200


def test_monthly_news_page__latest_month__search_by_country(
    db_no_rollback, client, latest_month, search_by_country
):
    response = client.get("%s?%s" % (latest_month, search_by_country))
    assert response.status_code == 200


def test_monthly_news_page__latest_month__search_by_state(
    db_no_rollback, client, latest_month, search_by_state
):
    response = client.get("%s?%s" % (latest_month, search_by_state))
    assert response.status_code == 200


def test_monthly_news_page__latest_month__search_by_county(
    db_no_rollback, client, latest_month, search_by_county
):
    response = client.get("%s?%s" % (latest_month, search_by_county))
    assert response.status_code == 200


def test_monthly_news_page__selected_month(  # noqa
    db_no_rollback, client, selected_month
):
    response = client.get(selected_month)
    assert response.status_code == 200


def test_monthly_news_page__selected_month__search_by_country(
    db_no_rollback, client, selected_month, search_by_country
):
    response = client.get("%s?%s" % (selected_month, search_by_country))
    assert response.status_code == 200


def test_monthly_news_page__selected_month__search_by_state(
    db_no_rollback, client, selected_month, search_by_state
):
    response = client.get("%s?%s" % (selected_month, search_by_state))
    assert response.status_code == 200


def test_monthly_news_page__selected_month__search_by_county(
    db_no_rollback, client, selected_month, search_by_county
):
    response = client.get("%s?%s" % (selected_month, search_by_county))
    assert response.status_code == 200
