import pytest


@pytest.fixture(scope="session")
def django_db_setup():
    # Don't create the local database. Instead, test against the existing one;
    # don't run any migrations;
    # don't tear down the database when the tests are finished.
    pass
