import json

from django.urls import reverse

import pytest

pytestmark = pytest.mark.django_db

redirects = [
    (reverse("index"), reverse("news:index")),
]

autocompletes = [
    reverse("filters:counties"),
    reverse("filters:states"),
    reverse("filters:counties"),
    reverse("filters:locations"),
    reverse("filters:observers"),
    reverse("filters:common-name"),
    reverse("filters:scientific-name"),
]

pages = [
    (reverse("news:index"), None),
    (reverse("checklists:list"), None),
    (reverse("observations:list"), None),
    (reverse("species:list"), None),
    (reverse("about"), None),
    (reverse("contact"), None),
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


@pytest.mark.parametrize("url", autocompletes)
def test_autocomplete_returns_data(client, url):
    response = client.get(url)
    json.loads(response.content)


@pytest.mark.parametrize("url,params", pages)
def test_page_is_displayed(client, url, params):
    response = client.get(url, query_params=params)
    assert response.status_code == 200


@pytest.mark.parametrize("url,status", errors)
def test_error_page_is_displayed(client, url, status):
    response = client.get(url)
    assert response.status_code == status
