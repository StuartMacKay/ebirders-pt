import datetime as dt

from django.urls import reverse


def test_weekly_news_page__current_week__displayed(db_no_rollback, client):
    response = client.get(reverse("news:monthly"))
    assert response.status_code == 200


def test_weekly_news_page__selected_week__displayed(db_no_rollback, client):
    today = dt.date.today()
    response = client.get(
        reverse(
            "news:for-month",
            kwargs={"year": today.year, "month": today.month},
        )
    )
    assert response.status_code == 200
