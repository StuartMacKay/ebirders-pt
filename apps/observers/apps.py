from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    name = "observers"
    verbose_name = _("Observers")

    def ready(self):
        from . import receivers  # noqa
