from django.urls import reverse


def test_checklists_list_url(db_no_rollback, client):
    url = reverse("checklists:list")
    assert client.get(url).status_code == 200
