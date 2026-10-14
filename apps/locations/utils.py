from django.core.cache import cache

from ebird.api.data.models import Country

COUNTRY_COUNT_KEY = "locations:country_count"


def get_country_count() -> int:
    # Cached since the template filter, show_country, is called for every
    # row in a table. The receivers clear it when a Country is added or
    # deleted.
    return cache.get_or_set(COUNTRY_COUNT_KEY, Country.objects.count, None)


def clear_country_count() -> None:
    cache.delete(COUNTRY_COUNT_KEY)
