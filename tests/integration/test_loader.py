from django.core.management import call_command

from faker import Faker
import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture()
def country():
    return Faker().country_code()


@pytest.fixture(autouse=True)
def mappings(settings, country):
    settings.EBIRD_LOCALES = {
        "en": "en",
    }
    settings.EBIRD_LEVELS = {
        country: {
            "subnational1": "district",
            "subnational2": "county",
        }
    }


def test_loader(country):
    call_command("load_api", "new", 2, country)
