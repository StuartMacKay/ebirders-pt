import datetime as dt

from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.utils.dateformat import format
from django.views import generic

from dateutil.relativedelta import relativedelta

from base.views import FormsMixin
from dates.forms import MonthFilter, WeekFilter
from locations.forms import RegionFilter
from notifications.models import Notification


class NewsView(FormsMixin, generic.TemplateView):
    template_name = "news/index.html"
    methods = ["GET", "HEAD"]
    form_classes = [RegionFilter, WeekFilter, MonthFilter]

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("news:index"), name))
        return urls

    def get_params(self, forms):
        params = {}
        for identifier, form in forms.items():
            params.update(form.get_params())
        return params

    @staticmethod
    def get_subtitle(start, finish):
        if start.year == finish.year:
            if start.month == finish.month:
                start_str = format(start, "d")
                finish_str = format(finish, "d M Y")
            else:
                start_str = format(start, "d M")
                finish_str = format(finish, "d M Y")
        else:
            start_str = format(start, "d M Y")
            finish_str = format(finish, "d M Y")

        subtitle = "%s - %s" % (start_str, finish_str)

        if translation.get_language() == "pt":
            subtitle = subtitle.lower()

        return subtitle

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.get_params(context["forms"])

        # Set default values for optional query params so pytest can
        # report undefined variables in the tests.

        if "country" not in params:
            params["country"] = None
        if "state" not in params:
            params["state"] = None
        if "county" not in params:
            params["county"] = None

        if "month" in params:
            subtitle = format(params["start"], "F Y")
        elif "week" in params:
            subtitle = self.get_subtitle(params["start"], params["finish"])
        else:  # Latest
            finish = dt.date.today()
            start = finish - relativedelta(days=6)
            params["start"] = start
            params["finish"] = finish
            params["year"] = finish.year
            subtitle = self.get_subtitle(start, finish)

        context.update(params)
        context["subtitle"] = subtitle
        context["translations"] = self.get_translations()
        context["notifications"] = Notification.objects.published()

        return context

    def handle_request(self, request, *args, **kwargs):
        forms = self.get_forms()
        [form.is_valid() for identifier, form in forms.items()]
        return self.forms_invalid(forms)

    def get(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)
