from django import forms
from django.contrib import admin
from django.contrib.admin import ModelAdmin, register
from django.utils.translation import gettext_lazy as _

from ebird.api.data.fields import TranslationCharField

from .fields import TranslationRichTextField
from .models import Update


class UpdateForm(forms.ModelForm):
    title = TranslationCharField()
    contents = TranslationRichTextField()

    class Meta:
        fields = "__all__"


@register(Update)
class UpdateAdmin(ModelAdmin):
    list_display = ("display_title", "published_at")
    search_fields = ("title",)
    ordering = ("-published_at",)
    form = UpdateForm

    @admin.display(description=_("Title"))
    def display_title(self, instance):
        return instance.get_title()
