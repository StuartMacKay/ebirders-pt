from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    label = "notifications"
    name = "notifications"
    verbose_name = _("Notifications")
