import json

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TranslationTextInput(forms.MultiWidget):
    template_name = "data/widgets/translation_field.html"

    def __init__(self, *args, **kwargs):
        widgets = [
            forms.TextInput(attrs={"locale": _(language), "style": "width: 100%"})
            for code, language in settings.LANGUAGES
        ]
        super().__init__(widgets, **kwargs)

    def decompress(self, value):
        if value:
            data = json.loads(value)
            return [data.get(code, "") for code, language in settings.LANGUAGES]
        return []


class TranslationTextarea(forms.MultiWidget):
    template_name = "data/widgets/translation_field.html"

    def __init__(self, *args, **kwargs):
        widgets = [
            forms.Textarea(attrs={"locale": _(language), "rows": 10, "cols": 40})
            for code, language in settings.LANGUAGES
        ]
        super().__init__(widgets, **kwargs)

    def decompress(self, value):
        if value:
            data = json.loads(value)
            return [data.get(code, "") for code, language in settings.LANGUAGES]
        return []
