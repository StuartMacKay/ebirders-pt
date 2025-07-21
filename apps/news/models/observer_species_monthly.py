import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


class ObserverSpeciesMonthly(models.Model):
    class Meta:
        db_table = "observer_species_monthly"
        verbose_name = _("ObserverSpeciesMonthly")
        verbose_name_plural = _("ObserverSpeciesMonthly")
        managed = False

    identifier = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name=_("identifier"),
        help_text=_("The unique identifier for the observation."),
    )

    observer = models.ForeignKey(
        "data.Observer",
        related_name="observer_species_monthly",
        on_delete=models.PROTECT,
        verbose_name=_("observer"),
        help_text=_("The person who made the observation."),
    )

    name = models.TextField(
        verbose_name=_("name"),
        help_text=_("The name of the observer."),
    )

    species = models.ForeignKey(
        "data.Species",
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("species"),
        help_text=_("The identified species."),
    )

    country = models.ForeignKey(
        "data.Country",
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("country"),
        help_text=_("The country where the observation was made."),
    )

    state = models.ForeignKey(
        "data.State",
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("state"),
        help_text=_("The state where the observation was made."),
    )

    county = models.ForeignKey(
        "data.County",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("county"),
        help_text=_("The county where the observation was made."),
    )

    year = models.IntegerField(
        db_index=True,
        verbose_name=_("year"),
        help_text=_("The year the observation was made."),
    )

    month = models.IntegerField(
        db_index=True,
        verbose_name=_("month"),
        help_text=_("The month the observation was made."),
    )

    def __repr__(self) -> str:
        return str(self.observer)

    def __str__(self) -> str:
        return str(self.observer)
