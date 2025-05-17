import datetime as dt

from django.urls import reverse


def test_weekly_news_page__current_week__displayed(db_no_rollback, client):
    response = client.get(reverse("news:weekly"))
    assert response.status_code == 200


def test_weekly_news_page__selected_week__displayed(db_no_rollback, client):
    today = dt.date.today()
    response = client.get(
        reverse(
            "news:for-week",
            kwargs={"year": today.year, "week": today.isocalendar().week},
        )
    )
    assert response.status_code == 200
