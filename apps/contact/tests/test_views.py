from django.urls import reverse


def test_contact_page__displayed(client):
    response = client.get(reverse("contact"))
    assert response.status_code == 200
