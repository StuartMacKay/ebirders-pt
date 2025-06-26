from django.urls import reverse


def test_list_view__is_displayed(db_no_rollback, client):
    url = reverse("events:list")
    response = client.get(url)
    assert response.status_code == 200


def test_list_view__is_paginated(db_no_rollback, client):
    url = reverse("events:list")
    response = client.get(url)
    view = response.context["view"]
    assert view.paginate_by is not None
