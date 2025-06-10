from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.db import models
from django.utils.translation import gettext_lazy as _

from data.fields import TranslationCharField, TranslationTextField

from .models import Update


class UpdateForm(forms.ModelForm):
    title = TranslationCharField()
    contents = TranslationTextField()

    class Meta:
        fields = "__all__"


@register(Update)
class UpdateAdmin(ModelAdmin):
    list_display = ("display_title", "published_at")
    search_fields = ("title",)
    ordering = ("-published_at",)
    form = UpdateForm

    formfield_overrides = {
        models.TextField: {"widget": forms.widgets.Textarea(attrs={"cols": "80"})},
    }

    @admin.display(description=_("Title"))
    def display_title(self, instance):
        return instance.get_title()
