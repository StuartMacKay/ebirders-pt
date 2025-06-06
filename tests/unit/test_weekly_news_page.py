import datetime as dt

from django.urls import reverse

import pytest


@pytest.fixture
def latest_week():
    return reverse("news:weekly")


@pytest.fixture
def selected_week():
    today = dt.date.today()
    return reverse(
        "news:for-week", kwargs={"year": today.year, "week": today.isocalendar().week}
    )


def test_weekly_news_page__latest_week(  # noqa
    db_no_rollback, client, latest_week
):
    response = client.get(latest_week)
    assert response.status_code == 200


def test_weekly_news_page__latest_week__search_by_country(
    db_no_rollback, client, latest_week, search_by_country
):
    response = client.get("%s?%s" % (latest_week, search_by_country))
    assert response.status_code == 200


def test_weekly_news_page__latest_week__search_by_state(
    db_no_rollback, client, latest_week, search_by_state
):
    response = client.get("%s?%s" % (latest_week, search_by_state))
    assert response.status_code == 200


def test_weekly_news_page__latest_week__search_by_county(
    db_no_rollback, client, latest_week, search_by_county
):
    response = client.get("%s?%s" % (latest_week, search_by_county))
    assert response.status_code == 200


def test_weekly_news_page__selected_week(  # noqa
    db_no_rollback, client, selected_week
):
    response = client.get(selected_week)
    assert response.status_code == 200


def test_weekly_news_page__selected_week__search_by_country(
    db_no_rollback, client, selected_week, search_by_country
):
    response = client.get("%s?%s" % (selected_week, search_by_country))
    assert response.status_code == 200


def test_weekly_news_page__selected_week__search_by_state(
    db_no_rollback, client, selected_week, search_by_state
):
    response = client.get("%s?%s" % (selected_week, search_by_state))
    assert response.status_code == 200


def test_weekly_news_page__selected_week__search_by_county(
    db_no_rollback, client, selected_week, search_by_county
):
    response = client.get("%s?%s" % (selected_week, search_by_county))
    assert response.status_code == 200
