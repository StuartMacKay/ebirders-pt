from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    ERRORS = {
        "message-required": _("You did not write a message."),
    }

    name = forms.CharField(required=False, label=_("Name"))
    email = forms.EmailField(required=False, label=_("Email"))
    message = forms.CharField(required=True, label=_("Message"), widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        field = self.fields["message"]
        field.error_messages["required"] = self.ERRORS["message-required"]

    def clean(self):
        cleaned_data = super().clean()
        for name in self._errors.keys():
            self.fields[name].widget.attrs["class"] += " is-invalid"
        return cleaned_data

    def error_count(self):
        return len(self.errors)
