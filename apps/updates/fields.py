from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ebird.api.data.fields import TranslationField

from .widgets import TranslationRichTextarea


class TranslationRichTextField(TranslationField):
    def __init__(self, **kwargs):
        fields = [
            forms.CharField(label=_(language)) for code, language in settings.LANGUAGES
        ]
        widget = TranslationRichTextarea
        super().__init__(fields=fields, widget=widget, **kwargs)
