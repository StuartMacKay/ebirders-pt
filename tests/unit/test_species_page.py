from django.urls import reverse

import pytest


def has_species(response) -> bool:
    return len(response.context["species_list"]) > 0


@pytest.fixture
def url():
    return reverse("species:list")


def test_species_page__displayed(db_no_rollback, client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_species_page__filtered_by_country(
    db_no_rollback, client, url, filter_by_country
):
    response = client.get("%s?%s" % (url, filter_by_country))
    assert has_species(response)


def test_species_page__filtered_by_state(
    db_no_rollback, client, url, filter_by_state
):
    response = client.get("%s?%s" % (url, filter_by_state))
    assert has_species(response)


def test_species_page__filtered_by_county(
    db_no_rollback, client, url, filter_by_county
):
    response = client.get("%s?%s" % (url, filter_by_county))
    assert has_species(response)


def test_species_page__filtered_by_observer(
    db_no_rollback, client, url, filter_by_observer
):
    response = client.get("%s?%s" % (url, filter_by_observer))
    assert has_species(response)


def test_species_page__filtered_by_start_date(
    db_no_rollback, client, url, filter_by_start_date
):
    response = client.get("%s?%s" % (url, filter_by_start_date))
    assert has_species(response)


def test_species_page__filtered_by_end_date(
    db_no_rollback, client, url, filter_by_end_date
):
    response = client.get("%s?%s" % (url, filter_by_end_date))
    assert has_species(response)


def test_species_page__filtered_by_date_range(
    db_no_rollback, client, url, filter_by_date_range
):
    response = client.get("%s?%s" % (url, filter_by_date_range))
    assert has_species(response)


def test_species_page__ordered_by_seen(
    db_no_rollback, client, url, ordered_by_seen
):
    response = client.get("%s?%s" % (url, ordered_by_seen))
    assert has_species(response)
