from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Refresh a materialized view"

    def add_arguments(self, parser):
        parser.add_argument(
            "views",
            nargs="+",
            type=str,
            help="The names of one or more materialized views to refresh",
        )

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            for view in options["views"]:
                cursor.execute("REFRESH MATERIALIZED VIEW %s;" % view)
