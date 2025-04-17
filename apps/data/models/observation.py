# pyright: reportArgumentType=false

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Observation(models.Model):
    class Meta:
        verbose_name = _("observation")
        verbose_name_plural = _("observations")

    edited = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("The date and time the eBird checklist was last edited"),
        verbose_name=_("edited"),
    )

    identifier = models.TextField(
        unique=True,
        verbose_name=_("identifier"),
        help_text=_("A global unique identifier for the observation."),
    )

    checklist = models.ForeignKey(
        "data.Checklist",
        related_name="observations",
        on_delete=models.CASCADE,
        verbose_name=_("checklist"),
        help_text=_("The checklist this observation belongs to."),
    )

    species = models.ForeignKey(
        "data.Species",
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("species"),
        help_text=_("The identified species."),
    )

    identified = models.BooleanField(
        verbose_name=_("identified"),
        help_text=_(
            "Was the species identified precisely, i.e. species or sub-species"
        ),
    )

    observer = models.ForeignKey(
        "data.Observer",
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("observer"),
        help_text=_("The person who made the observation."),
    )

    country = models.ForeignKey(
        "data.Country",
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("country"),
        help_text=_("The country where the observation was made."),
    )

    region = models.ForeignKey(
        "data.Region",
        blank=True,
        null=True,
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("region"),
        help_text=_("The region where the observation was made."),
    )

    state = models.ForeignKey(
        "data.State",
        blank=True,
        null=True,
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("state"),
        help_text=_("The state where the observation was made."),
    )

    district = models.ForeignKey(
        "data.District",
        blank=True,
        null=True,
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("district"),
        help_text=_("The district where the observation was made."),
    )

    county = models.ForeignKey(
        "data.County",
        blank=True,
        null=True,
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("county"),
        help_text=_("The county where the observation was made."),
    )

    area = models.ForeignKey(
        "data.Area",
        blank=True,
        null=True,
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("area"),
        help_text=_("The area where the observation was made."),
    )

    location = models.ForeignKey(
        "data.Location",
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("location"),
        help_text=_("The location where the observation was made."),
    )

    date = models.DateField(
        db_index=True,
        verbose_name=_("date"),
        help_text=_("The date the observation was made."),
    )

    time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_("time"),
        help_text=_("The time the observation was made."),
    )

    started = models.DateTimeField(
        blank=True,
        db_index=True,
        null=True,
        verbose_name=_("date & time"),
        help_text=_("The date and time the observation was made."),
    )

    count = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("count"),
        help_text=_("The number of birds seen."),
    )

    breeding_code = models.TextField(
        blank=True,
        verbose_name=_("breeding code"),
        help_text=_("eBird code identifying the breeding status"),
    )

    breeding_category = models.TextField(
        blank=True,
        verbose_name=_("breeding category"),
        help_text=_("eBird code identifying the breeding category"),
    )

    behavior_code = models.TextField(
        blank=True,
        verbose_name=_("behaviour code"),
        help_text=_("eBird code identifying the behaviour"),
    )

    age_sex = models.TextField(
        blank=True,
        verbose_name=_("Age & Sex"),
        help_text=_("The number of birds seen in each combination of age and sex."),
    )

    media = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_("has media"),
        help_text=_("Has audio, photo or video uploaded to the Macaulay library."),
    )

    approved = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_("Approved"),
        help_text=_("Has the observation been accepted by eBird's review process."),
    )

    reviewed = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_("Reviewed"),
        help_text=_("Was the observation reviewed because it failed automatic checks."),
    )

    reason = models.TextField(
        blank=True,
        verbose_name=_("Reason"),
        help_text=_(
            "The reason given for the observation to be marked as not confirmed."
        ),
    )

    comments = models.TextField(
        blank=True,
        verbose_name=_("comments"),
        help_text=_("Any comments about the observation."),
    )

    urn = models.TextField(
        blank=True,
        verbose_name=_("URN"),
        help_text=_("The globally unique identifier for the observation"),
    )

    data = models.JSONField(
        verbose_name=_("Data"),
        help_text=_("Data describing an Observation."),
        default=dict,
        blank=True,
    )

    def __repr__(self) -> str:
        return str(self.identifier)

    def __str__(self) -> str:
        return str(self.identifier)
