import logging

from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, mail_managers
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views import generic

from .forms import ContactForm

log = logging.getLogger(__name__)


class ContactView(generic.FormView):
    form_class = ContactForm
    template_name = "contact/form.html"
    success_url = reverse_lazy("contact")

    message_template_name = "contact/email.txt"

    MESSAGES = {
        "sent-without-email": _("Thanks for your message."),
        "sent-with-email": _("Thanks for your message. You will get a reply shortly."),
        "not-sent": _("Your message could not be sent. Please try again later."),
    }

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("contact"), name))
        return urls

    def form_valid(self, form):
        if self.send_message(form):
            if form.cleaned_data.get("email"):
                messages.success(self.request, self.MESSAGES["sent-with-email"])
            else:
                messages.success(self.request, self.MESSAGES["sent-without-email"])
            return super().form_valid(form)
        else:
            messages.error(self.request, self.MESSAGES["not-sent"])
            return super().form_invalid(form)

    def get_message(self, form) -> str:
        return get_template(self.message_template_name).render(form.cleaned_data)

    def send_message(self, form) -> bool:  # noqa
        try:
            subject = "Contact form submitted."
            message = self.get_message(form)
            mail_managers(subject, message)
            sent = True
        except (BadHeaderError, SMTPException, IOError):
            log.exception("Notification not sent")
            sent = False
        return sent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["translations"] = self.get_translations()
        return context
