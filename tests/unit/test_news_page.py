from django.urls import reverse

import pytest 


@pytest.fixture
def url():
    return reverse("news:index")


def test_news_page__displayed(db_no_rollback, client, url):
    response = client.get(url)
    assert response.status_code == 200