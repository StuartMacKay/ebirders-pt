import os

from django.conf import settings

import polib

import pytest


def list_strings(entries):
    # Show strings in quotes to catch string with leading/trailing whitespace
    return "\n".join(['"%s"' % entry.msgid for entry in entries])


def strings_files():
    return [os.path.join(
        settings.ROOT_DIR,
        "locale/%s/LC_MESSAGES/django.po" % code
    ) for code, name in settings.LANGUAGES]


@pytest.mark.parametrize("path", strings_files())
def test_for_untranslated_strings(path):
    """Verify that all strings have been translated."""
    pofile = polib.pofile(path)
    entries = pofile.untranslated_entries()
    assert not entries, list_strings(entries)


@pytest.mark.parametrize("path", strings_files())
def test_for_fuzzy_strings(path):
    """Verify that no strings are marked as fuzzy."""
    pofile = polib.pofile(path)
    entries = pofile.fuzzy_entries()
    assert not entries, list_strings(entries)


@pytest.mark.parametrize("path", strings_files())
def test_for_obsolete_strings(path):
    """Verify that no strings are marked as obsolete."""
    pofile = polib.pofile(path)
    entries = pofile.obsolete_entries()
    assert not entries, list_strings(entries)
