from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    label = "_species"
    name = "species"
    verbose_name = _("species.plural")
