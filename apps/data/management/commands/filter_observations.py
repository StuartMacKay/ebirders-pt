from django.core.management.base import BaseCommand

from data.models import Checklist, Filter, Observation


class Command(BaseCommand):
    help = "Run filters on observations loaded from the eBird API"

    def handle(self, *args, **options):
        for filter in Filter.objects.filter(enabled=True):
            filter.apply()

        Checklist.objects.filter(published=False).update(published=True)
        Observation.objects.filter(published=False).update(published=True)
