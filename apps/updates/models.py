import json
import logging

from json import JSONDecodeError

from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


class UpdateManager(models.Manager):

    def published(self):
        return self.filter(published_at__isnull=False, published_at__lt=timezone.now())


class Update(models.Model):
    class Meta:
        verbose_name = _("Update")
        verbose_name_plural = _("Updates")

    published_at = models.DateTimeField(
        verbose_name=_("Published"),
        help_text=_("The date the Update was published. May be in the future"),
        blank=True,
        null=True,
    )

    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("The title of the Update"),
        max_length=100,
    )

    contents = models.TextField(
        verbose_name=_("Contents"),
        help_text=_("The contents of the Update. HTML is allowed"),
    )

    objects = UpdateManager()

    def __str__(self):
        return str(self.title)

    def get_title(self):
        try:
            data = json.loads(self.title)
            title = data.get(get_language(), "")
        except JSONDecodeError:
            log.error("Incorrect JSON for Update contents: %s", self.id)
            title = ""
        return mark_safe(title)

    def get_contents(self):
        try:
            data = json.loads(self.contents)
            contents = data.get(get_language(), "")
        except JSONDecodeError:
            log.error("Incorrect JSON for Update contents: %s", self.id)
            contents = ""
        return mark_safe(contents)
