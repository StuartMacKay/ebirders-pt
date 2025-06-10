from django.urls import reverse


def test_updates_page__displayed(db_no_rollback, client):
    response = client.get(reverse("updates:list"))
    assert response.status_code == 200
