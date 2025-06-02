from django.contrib.admin import ModelAdmin, register
from django.db import models
from django.forms import ModelForm, widgets

from data.fields import TranslationTextField

from .models import Notification


class NotificationForm(ModelForm):
    contents = TranslationTextField()

    class Meta:
        fields = '__all__'


@register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ("title", "level", "published", "expired")

    list_filter = ("level",)

    form = NotificationForm

    search_fields = ("title",)

    ordering = ("-published",)

    formfield_overrides = {
        models.TextField: {"widget": widgets.Textarea(attrs={"cols": "80"})},
    }
