from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db

redirects = [
    (reverse("index"), reverse("news:latest")),
]

urls = [
    (reverse("news:latest"), None),
    (reverse("news:weekly"), None),
    (reverse("news:monthly"), None),
    (reverse("checklists:list"), None),
    (reverse("observations:list"), None),
    (reverse("species:list"), None),
]

errors = [
    ("/403/", 403),
    ("/404/", 404),
    ("/500/", 500),
]


@pytest.mark.parametrize("url,redirect", redirects)
def test_page_redirects(client, url, redirect):
    response = client.get(url, follow=False)
    assert response.url == redirect


@pytest.mark.parametrize("url,params", urls)
def test_page_is_displayed(client, url, params):
    response = client.get(url, query_params=params)
    assert response.status_code == 200


@pytest.mark.parametrize("url,status", errors)
def test_error_page_is_displayed(client, url, status):
    response = client.get(url)
    assert response.status_code == status
