import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


class Event(models.Model):
    class Type(models.IntegerChoices):
        OBSERVATION_REJECTED = 1, _("Observation rejected")
        OBSERVATION_REVIEWED = 2, _("Observation reviewed")

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date and time the event occurred"),
        verbose_name=_("created"),
    )

    type = models.IntegerField(
        choices=Type.choices,
        verbose_name=_("type"),
        help_text=_("The type of event that occurred.")
    )

    observation = models.ForeignKey(
        "data.Observation",
        related_name="events",
        on_delete=models.CASCADE,
        verbose_name=_("observation"),
        help_text=_("The Observation associated with this event."),
    )

    data = models.JSONField(
        blank=True,
        default=dict,
        verbose_name=_("Data"),
        help_text=_("Data describing the Event."),
    )

    def __repr__(self) -> str:
        return str(self.type)

    def __str__(self) -> str:
        return str(self.type)
