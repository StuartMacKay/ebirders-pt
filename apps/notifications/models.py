import json
import logging

from json import JSONDecodeError

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


class NotificationManager(models.Manager):
    def published(self):
        now = timezone.now()
        return self.filter(published__isnull=False, published__lt=now).exclude(
            expired__isnull=False, expired__lt=now
        )

    def expired(self):
        now = timezone.now()
        return self.filter(expired__isnull=False, expired__lt=now)


class Notification(models.Model):
    class Level(models.TextChoices):
        INFO = "info", _("Info")
        SUCCESS = "success", _("Success")
        WARNING = "warning", _("Warning")
        DANGER = "danger", _("Danger")

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    published = models.DateTimeField(
        verbose_name=_("Published"),
        help_text=_("The date the Notification was published. May be in the future"),
        blank=True,
        null=True,
    )

    expired = models.DateTimeField(
        verbose_name=_("Expired"),
        help_text=_("The date the Notification will expire and no longer be available"),
        blank=True,
        null=True,
    )

    level = models.CharField(
        choices=Level.choices,
        help_text=_("The alert level for the notification"),
        max_length=20,
    )

    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("The title of the Notification"),
        max_length=100,
    )

    contents = models.TextField(
        verbose_name=_("Contents"),
        help_text=_("The contents of the Notification"),
    )

    data = models.JSONField(
        verbose_name=_("Data"),
        help_text=_("Data describing a Notification."),
        default=dict,
        blank=True,
    )

    objects = NotificationManager()

    def __str__(self):
        return str(self.title)

    def get_contents(self):
        try:
            data = json.loads(self.contents)
            contents = data.get(get_language(), "")
        except JSONDecodeError:
            log.error("Incorrect JSON for Notification contents: %s", self.id)
            contents = ""
        return mark_safe(contents)
