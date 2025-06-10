from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from data.fields import TranslationCharField, TranslationTextField

from .models import Notification


class NotificationForm(ModelForm):
    title = TranslationCharField()
    contents = TranslationTextField()

    class Meta:
        fields = '__all__'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("display_title", "level", "published", "expired")

    list_filter = ("level",)

    form = NotificationForm

    search_fields = ("title",)

    ordering = ("-published",)

    @admin.display(description=_("Title"))
    def display_title(self, instance):
        return instance.get_title()
