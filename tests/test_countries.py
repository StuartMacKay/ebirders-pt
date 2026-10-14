from django.core.cache import cache
from django.urls import reverse

import pytest
from ebird.api.data.models import Checklist, Country

from locations.forms import RegionFilter
from locations.templatetags.locations import show_country
from locations.utils import get_country_count

pytestmark = pytest.mark.django_db

# Pages which show the country for each checklist or observation, and the
# region filter, with the country dropdown.
pages = [
    reverse("news:index"),
    reverse("checklists:list"),
    reverse("observations:list"),
    reverse("species:list"),
]


@pytest.fixture(autouse=True)
def local_cache(settings):
    # Use a real cache, so caching the count can be tested, rather than
    # the dummy cache usually used in development. Clear it before and
    # after each test since adding a country is rolled back without the
    # post_delete signal being sent, and the news page is cached.
    settings.CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
    }
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def country():
    if Country.objects.count() != 1:
        pytest.skip("The database must contain checklists for one country.")
    return Country.objects.get()


@pytest.fixture
def second_country(country):
    return Country.objects.create(code="XX", name="Elsewhere", place="Elsewhere")


def test_country_count():
    assert get_country_count() == Country.objects.count()


def test_country_count_is_cached(django_assert_num_queries):
    get_country_count()
    with django_assert_num_queries(0):
        get_country_count()


def test_adding_country_clears_count(country):
    assert get_country_count() == 1
    Country.objects.create(code="XX", name="Elsewhere", place="Elsewhere")
    assert get_country_count() == 2


def test_deleting_country_clears_count(second_country):
    assert get_country_count() == 2
    second_country.delete()
    assert get_country_count() == 1


def test_country_hidden_for_one_country(country):
    assert not show_country(country)


def test_country_shown_for_two_countries(country, second_country):
    assert show_country(country)
    assert show_country(second_country)


def test_filter_has_no_country_for_one_country(country):
    form = RegionFilter()
    assert "country" not in form.fields
    assert "state" in form.fields
    assert "county" in form.fields


def test_filter_has_country_for_two_countries(second_country):
    form = RegionFilter()
    assert "country" in form.fields
    assert "state" in form.fields
    assert "county" in form.fields


def test_filter_ignores_country_for_one_country(country):
    form = RegionFilter(data={"country": [country.code]})
    assert form.is_valid()
    assert form.get_filters() == {}


@pytest.mark.parametrize("url", pages)
def test_page_for_one_country(client, country, url):
    if not Checklist.objects.exists():
        pytest.skip("Load some checklists first.")
    content = client.get(url).content.decode()
    assert 'name="country"' not in content
    assert 'name="state"' in content
    assert "country=%s" % country.code not in content


@pytest.mark.parametrize("url", pages)
def test_page_for_two_countries(client, second_country, url):
    if not Checklist.objects.exists():
        pytest.skip("Load some checklists first.")
    content = client.get(url).content.decode()
    assert 'name="country"' in content
    assert 'name="state"' in content
