import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from .observation import Observation

log = logging.getLogger(__name__)


class Filter(models.Model):
    class Meta:
        verbose_name = _("filter")
        verbose_name_plural = _("filters")

    enabled = models.BooleanField(
        help_text=_("Is the filter active?"),
        verbose_name=_("enabled"),
    )

    name = models.TextField(
        verbose_name=_("name"), help_text=_("The name of the filter.")
    )

    initial_species = models.ForeignKey(
        "data.Species",
        related_name="filtered_on",
        on_delete=models.CASCADE,
        verbose_name=_("initial species"),
        help_text=_("The species used to find matching Observations."),
    )

    result_species = models.ForeignKey(
        "data.Species",
        related_name="filtered_by",
        on_delete=models.CASCADE,
        verbose_name=_("result species"),
        help_text=_("Matching Observations are updated to this species."),
    )

    def __repr__(self) -> str:
        return str(self.name)

    def __str__(self) -> str:
        return str(self.name)

    def apply(self):
        log.info("Applying filter: %s", self.name)
        count = 0
        for observation in Observation.objects.filter(species=self.initial_species):
            observation.species = self.result_species
            observation.save()
            count += 1
        log.info("Observations updated: %d", count)
