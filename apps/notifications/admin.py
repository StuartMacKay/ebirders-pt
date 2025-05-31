from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.db import models
from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import Notification


@register(Notification)
class NotificationAdmin(ModelAdmin):

    list_display = ("title", "level", "published", "expired")

    list_filter = ("level",)

    search_fields = ("title",)

    ordering = ("-published",)

    formfield_overrides = {
        models.TextField: {"widget": widgets.Textarea(attrs={"cols": "80"})},
    }

    @admin.display(description=_("Formatted"))
    def pretty_contents(self, instance):
        return mark_safe(instance.contents)
