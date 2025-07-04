from django.core.management import call_command

from data.models import Country

import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture()
def country():
    return Country.objects.first()


def test_loader(db_no_rollback, country):
    call_command("add_checklists", "--days", 2, country.code)
