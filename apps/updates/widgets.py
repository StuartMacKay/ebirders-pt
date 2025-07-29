from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ckeditor.fields import CKEditorWidget
from ebird.api.data.widgets import TranslationTextarea


class TranslationRichTextarea(TranslationTextarea):
    def __init__(self, **kwargs):
        widgets = [
            CKEditorWidget(attrs={"locale": _(language)})
            for code, language in settings.LANGUAGES
        ]
        super().__init__(widgets=widgets, **kwargs)
