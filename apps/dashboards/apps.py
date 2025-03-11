from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    label = "_dashboards"
    name = "dashboards"
    verbose_name = _("Dashboards")
