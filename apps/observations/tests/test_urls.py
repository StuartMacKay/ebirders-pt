from django.urls import reverse


def test_observations_list_url(db_no_rollback, client):
    url = reverse("observations:list")
    assert client.get(url).status_code == 200
