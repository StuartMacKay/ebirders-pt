import datetime as dt
import re

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils import translation
from django.utils.dateformat import format
from django.views import generic

from dateutil.relativedelta import relativedelta
from ebird.codes.locations import is_country_code, is_county_code, is_state_code

from data.models import Country, County, State
from notifications.models import Notification


class LatestView(generic.TemplateView):
    template_name = "news/latest.html"

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("news:latest"), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        start_date = dt.date.today() - relativedelta(days=6)
        end_date = dt.date.today()

        if start_date.month == end_date.month:
            subtitle = "%s - %s" % (format(start_date, "d"), format(end_date, "d M Y"))
        else:
            if start_date.year == end_date.year:
                subtitle = "%s - %s" % (
                    format(start_date, "d M"),
                    format(end_date, "d M Y"),
                )
            else:
                subtitle = "%s - %s" % (
                    format(start_date, "d M Y"),
                    format(end_date, "d M Y"),
                )

        if translation.get_language() == "pt":
            subtitle = subtitle.lower()

        code = self.request.GET.get("code", "")
        search = self.request.GET.get("search", "")
        country = state = county = None

        if is_country_code(code):
            country = Country.objects.get(code=code)
        elif is_state_code(code):
            state = State.objects.get(code=code)
        elif is_county_code(code):
            county = County.objects.get(code=code)

        context["interval"] = "latest"
        context["code"] = county
        context["search"] = search
        context["country"] = country
        context["state"] = state
        context["county"] = county
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["start_year"] = start_date.replace(month=1, day=1)
        context["end_year"] = end_date.replace(month=12, day=31)
        context["subtitle"] = subtitle
        context["show_country"] = Country.objects.count() > 1
        context["translations"] = self.get_translations()
        context["notifications"] = Notification.objects.published()
        return context


class WeeklyView(generic.TemplateView):
    template_name = "news/weekly.html"

    @staticmethod
    def get_translations(year, week):
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("news:for-week", args=(year, week)), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        year = self.kwargs.get("year", dt.date.today().year)
        week = self.kwargs.get("week", dt.date.today().isocalendar().week - 1)

        start_date = dt.datetime.strptime("%d-%d-1" % (year, week), "%Y-%W-%w").date()
        end_date = start_date + dt.timedelta(days=6)

        if start_date.month == end_date.month:
            subtitle = "%s - %s" % (format(start_date, "d"), format(end_date, "d M Y"))
        else:
            if start_date.year == end_date.year:
                subtitle = "%s - %s" % (
                    format(start_date, "d M"),
                    format(end_date, "d M Y"),
                )
            else:
                subtitle = "%s - %s" % (
                    format(start_date, "d M Y"),
                    format(end_date, "d M Y"),
                )

        next_start_date = start_date + dt.timedelta(days=7)
        next_end_date = end_date + dt.timedelta(days=7)
        next_year = next_start_date.year
        next_week = next_start_date.isocalendar().week - 1

        if next_start_date.month == next_end_date.month:
            next_label = "%s - %s" % (format(next_start_date, "d"), format(next_end_date, "d M Y"))
        else:
            if next_start_date.year == next_end_date.year:
                next_label = "%s - %s" % (
                    format(next_start_date, "d M"),
                    format(next_end_date, "d M Y"),
                )
            else:
                next_label = "%s - %s" % (
                    format(next_start_date, "d M Y"),
                    format(next_end_date, "d M Y"),
                )

        previous_start_date = start_date - dt.timedelta(days=7)
        previous_end_date = end_date - dt.timedelta(days=7)
        previous_year = previous_start_date.year
        previous_week = previous_start_date.isocalendar().week - 1

        if previous_start_date.month == previous_end_date.month:
            previous_label = "%s - %s" % (format(previous_start_date, "d"), format(previous_end_date, "d M Y"))
        else:
            if previous_start_date.year == previous_end_date.year:
                previous_label = "%s - %s" % (
                    format(previous_start_date, "d M"),
                    format(previous_end_date, "d M Y"),
                )
            else:
                previous_label = "%s - %s" % (
                    format(previous_start_date, "d M Y"),
                    format(previous_end_date, "d M Y"),
                )

        if translation.get_language() == "pt":
            subtitle = subtitle.lower()
            previous_label = previous_label.lower()
            next_label = next_label.lower()

        code = self.request.GET.get("code", "")
        search = self.request.GET.get("search", "")
        country = state = county = None

        if is_country_code(code):
            country = Country.objects.get(code=code)
        elif is_state_code(code):
            state = State.objects.get(code=code)
        elif is_county_code(code):
            county = County.objects.get(code=code)

        context["interval"] = "week"
        context["code"] = county
        context["search"] = search
        context["country"] = country
        context["state"] = state
        context["county"] = county
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["start_year"] = start_date.replace(month=1, day=1)
        context["end_year"] = end_date.replace(month=12, day=31)
        context["previous_year"] = previous_year
        context["previous_week"] = previous_week
        context["previous_label"] = previous_label
        context["next_year"] = next_year
        context["next_week"] = next_week
        context["next_label"] = next_label
        context["subtitle"] = subtitle
        context["show_country"] = Country.objects.count() > 1
        context["translations"] = self.get_translations(year, week)

        return context


class MonthlyView(generic.TemplateView):
    template_name = "news/monthly.html"

    @staticmethod
    def get_translations(year, month):
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("news:for-month", args=(year, month)), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        year = self.kwargs.get("year", dt.date.today().year)
        month = self.kwargs.get("month", dt.date.today().month)

        start_date = dt.date(year=year, month=month, day=1)
        end_date = start_date + relativedelta(months=1, days=-1)

        subtitle = format(start_date, "F Y")

        next_date = start_date + relativedelta(months=1)
        next_year = next_date.year
        next_month = next_date.month
        next_label = format(next_date, "F Y")

        previous_date = start_date - relativedelta(months=1)
        previous_year = previous_date.year
        previous_month = previous_date.month
        previous_label = format(previous_date, "F Y")

        if translation.get_language() == "pt":
            subtitle = subtitle.lower()
            previous_label = previous_label.lower()
            next_label = next_label.lower()

        code = self.request.GET.get("code", "")
        search = self.request.GET.get("search", "")
        country = state = county = None

        if is_country_code(code):
            country = Country.objects.get(code=code)
        elif is_state_code(code):
            state = State.objects.get(code=code)
        elif is_county_code(code):
            county = County.objects.get(code=code)

        context["interval"] = "month"
        context["code"] = county
        context["search"] = search
        context["country"] = country
        context["state"] = state
        context["county"] = county
        context["start_date"] = start_date
        context["end_date"] = end_date
        context["start_year"] = start_date.replace(month=1, day=1)
        context["end_year"] = end_date.replace(month=12, day=31)
        context["previous_label"] = previous_label
        context["previous_year"] = previous_year
        context["previous_month"] = previous_month
        context["next_label"] = next_label
        context["next_year"] = next_year
        context["next_month"] = next_month
        context["subtitle"] = subtitle
        context["show_country"] = Country.objects.count() > 1
        context["translations"] = self.get_translations(year, month)

        return context


def autocomplete(request):
    """
    Return the list of countries, states, and counties for the search field.
    If there is only one country, remove it from the label.
    """
    data = []

    for code, place in Country.objects.all().values_list("code", "place"):
        data.append({"value": code, "label": place})

    if len(data) == 1:
        country = data.pop(0)["label"]
    else:
        country = None

    for code, place in State.objects.all().values_list("code", "place"):
        if country:
            label = re.sub(r", %s$" % country, "", place)
        else:
            label = place
        data.append({"value": code, "label": label})

    for code, place in County.objects.all().values_list("code", "place"):
        if country:
            label = re.sub(r", %s$" % country, "", place)
        else:
            label = place
        data.append({"value": code, "label": label})

    return JsonResponse(data, safe=False)
