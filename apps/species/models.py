import json
import logging

from json import JSONDecodeError

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from ebird.api.data.models import Species

log = logging.getLogger(__name__)


class SpeciesList(models.Model):
    class Meta:
        abstract = True

    identifier = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name=_("identifier"),
        help_text=_("The unique identifier for the observation."),
    )

    checklist = models.ForeignKey(
        "data.Checklist",
        related_name="+",
        on_delete=models.CASCADE,
        verbose_name=_("checklist"),
        help_text=_("The checklist this observation belongs to."),
    )

    species = models.ForeignKey(
        "data.Species",
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("species"),
        help_text=_("The identified species."),
    )

    category = models.TextField(
        blank=True,
        choices=Species.Category,
        verbose_name=_("category"),
        help_text=_("The category from the eBird/Clements taxonomy."),
    )

    observer = models.ForeignKey(
        "data.Observer",
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("observer"),
        help_text=_("The person who made the observation."),
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
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("county"),
        help_text=_("The county where the observation was made."),
    )

    location = models.ForeignKey(
        "data.Location",
        related_name="+",
        on_delete=models.PROTECT,
        verbose_name=_("location"),
        help_text=_("The location where the observation was made."),
    )

    date = models.DateField(
        db_index=True,
        verbose_name=_("date"),
        help_text=_("The date the observation was made."),
    )

    started = models.DateTimeField(
        blank=True,
        db_index=True,
        null=True,
        verbose_name=_("date & time"),
        help_text=_("The date and time the observation was made."),
    )

    year = models.IntegerField(
        db_index=True,
        verbose_name=_("year"),
        help_text=_("The year the observation was made."),
    )

    count = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=_("count"),
        help_text=_("The number of birds seen."),
    )

    approved = models.BooleanField(
        default=True,
        verbose_name=_("Approved"),
        help_text=_("Has the observation been accepted."),
    )

    reason = models.TextField(
        blank=True,
        verbose_name=_("Reason"),
        help_text=_(
            "The reason given for the observation to be marked as not approved."
        ),
    )

    def __repr__(self) -> str:
        return str(self.species)

    def __str__(self) -> str:
        return str(self.species)

    def get_reason(self) -> str:
        try:
            data = json.loads(self.reason)
            reason = data.get(get_language(), "")
        except JSONDecodeError:
            log.error("Incorrect JSON for Observation reason: %s", self.id)
            reason = ""
        return reason


class CountryList(SpeciesList):
    class Meta:
        db_table = "country_list"
        verbose_name = _("Country List")
        verbose_name_plural = _("Country Lists")
        managed = False


class StateList(SpeciesList):
    class Meta:
        db_table = "state_list"
        verbose_name = _("State List")
        verbose_name_plural = _("State Lists")
        managed = False


class CountyList(SpeciesList):
    class Meta:
        db_table = "county_list"
        verbose_name = _("County List")
        verbose_name_plural = _("County Lists")
        managed = False
