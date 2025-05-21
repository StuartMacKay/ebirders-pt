from django.db import models
from django.utils.translation import gettext_lazy as _


class Observer(models.Model):
    class Meta:
        verbose_name = _("observer")
        verbose_name_plural = _("observers")

    identifier = models.TextField(
        verbose_name=_("identifier"),
        help_text=_("The code for the person submitted the checklist."),
    )

    name = models.TextField(
        blank=True,
        unique=True,
        verbose_name=_("name"),
        help_text=_("The observer's name."),
    )

    byname = models.TextField(
        blank=True,
        verbose_name=_("byname"),
        help_text=_("The display name of the observer"),
    )

    multiple = models.BooleanField(
        default=False,
        verbose_name=_("Multiple accounts"),
        help_text=_("Is the name used by more than one eBird account."),
    )

    enabled = models.BooleanField(
        default=True,
        verbose_name=_("Enabled"),
        help_text=_("Load checklists from the eBird observer."),
    )

    data = models.JSONField(
        verbose_name=_("Data"),
        help_text=_("Data describing an Observer."),
        default=dict,
        blank=True,
    )

    def __repr__(self) -> str:
        return str(self.identifier)

    def __str__(self) -> str:
        return str(self.name)

    def display_name(self):
        return str(self.byname or self.name)
