from django.urls import reverse


def test_species_list_url(db_no_rollback, client):
    url = reverse("species:list")
    assert client.get(url).status_code == 200
