"""
load_species.py

A Django management command for loading taxonomy information from the eBird API.

Modes:
    common_names  Load the common names for each entry in the LANGUAGES setting

Usage:
    python manage.py load_species common_names

This the common name for each language into a dictionary stored in the
Species.data attribute. For example:

    {
        "common_name": {
            "en": "Cory's Shearwater",
            "pt": "Cagarra",
        }
    }

The species common name for the currently activated language can then be
displayed in a template using:

    {% load species_tags %}
    {% get_current_language as language_code %}

    {% get_common_name observation.species language_code %}


NOTES:

    1. When checklists are loaded from the eBird API, the Species.common_name
       attribute is set using the EBIRD_LOCALE setting. That is sufficient for
       single language sites. For sites supporting multiple languages you can
       periodically load the translations using a scheduler such as cron. If you
       use the absolute paths to python and the command, then you don't need
       to deal with activating the virtual environment, for example:

       # At midnight Load missing translations for species common names
       0 0 * * * /home/me/my-project/.venv/bin/python /home/me/my-project/manage.py load_species common_name

"""

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from ebird.checklists.models import Species
from ebird.api import get_taxonomy

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load translations for species names from the eBird taxonomy"

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            title="sub-commands",
            required=True,
        )

        common_names_parser = subparsers.add_parser(
            "common_names",
            help="Load common names.",
        )
        common_names_parser.set_defaults(method=self.common_names)

    def handle(self, *args, method, **options):
        method(*args, **options)

    def common_names(self, **options) -> None:
        logger.info("Loading species common names")

        for species in Species.objects.all():
            if not species.data:
                species.data = {}
            if "common_name" not in species.data:
                species.data["common_name"] = {}

            for locale, name in settings.LANGUAGES:
                if locale in species.data["common_name"]:
                    continue

                logger.info(
                    "Loading common name: %s, %s",
                    species.species_code, locale,
                    extra={
                        "species_code": species.species_code,
                        "locale": locale,
                    },
                )

                data = get_taxonomy(
                    settings.EBIRD_API_KEY,
                    locale=settings.EBIRD_LANGUAGES[locale],
                    species=species.species_code
                )[0]

                species.data["common_name"][locale] = data["comName"]
                species.save()

        logger.info("Loading species common names succeeded")
