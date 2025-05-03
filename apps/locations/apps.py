from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "locations"
    verbose_name = _("Locations")

    def ready(self):
        from . import receivers  # noqa
