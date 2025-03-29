from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    label = "news"
    name = "news"
    verbose_name = _("News")
