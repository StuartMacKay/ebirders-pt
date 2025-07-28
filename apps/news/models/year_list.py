import json
import logging

from json import JSONDecodeError

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


class YearList(models.Model):
    class Meta:
        db_table = "year_list"
        verbose_name = _("YearList")
        verbose_name_plural = _("YearLists")
        managed = False

    identifier = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name=_("identifier"),
        help_text=_("The unique identifier for the observation."),
    )

    checklist = models.ForeignKey(
        "data.Checklist",
        related_name="yearlists",
        on_delete=models.CASCADE,
        verbose_name=_("checklist"),
        help_text=_("The checklist this observation belongs to."),
    )

    species = models.ForeignKey(
        "data.Species",
        related_name="yearlists",
        on_delete=models.PROTECT,
        verbose_name=_("species"),
        help_text=_("The identified species."),
    )

    observer = models.ForeignKey(
        "data.Observer",
        related_name="yearlists",
        on_delete=models.PROTECT,
        verbose_name=_("observer"),
        help_text=_("The person who made the observation."),
    )

    country = models.ForeignKey(
        "data.Country",
        related_name="yearlists",
        on_delete=models.PROTECT,
        verbose_name=_("country"),
        help_text=_("The country where the observation was made."),
    )

    state = models.ForeignKey(
        "data.State",
        related_name="yearlists",
        on_delete=models.PROTECT,
        verbose_name=_("state"),
        help_text=_("The state where the observation was made."),
    )

    county = models.ForeignKey(
        "data.County",
        blank=True,
        null=True,
        related_name="yearlists",
        on_delete=models.PROTECT,
        verbose_name=_("county"),
        help_text=_("The county where the observation was made."),
    )

    location = models.ForeignKey(
        "data.Location",
        related_name="yearlists",
        on_delete=models.PROTECT,
        verbose_name=_("location"),
        help_text=_("The location where the observation was made."),
    )

    date = models.DateField(
        db_index=True,
        verbose_name=_("date"),
        help_text=_("The date the observation was made."),
    )

    # year = models.IntegerField(
    #     db_index=True,
    #     verbose_name=_("year"),
    #     help_text=_("The year the observation was made."),
    # )

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
