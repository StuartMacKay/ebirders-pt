import datetime as dt

from dateutil.relativedelta import relativedelta, MO

from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateformat import format
from django.utils.translation import gettext_lazy as _
from django.views import generic

from ebird.codes.locations import is_country_code, is_state_code, is_county_code

from checklists.models import Checklist, Country, District, Region


class IndexView(generic.TemplateView):
    template_name = "dashboards/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if date_str := self.request.GET.get("date"):
            date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            date = timezone.now().date()

        today = timezone.now().date()
        report = self.request.GET.get("report", "daily")
        code = self.request.GET.get("code", "")
        place = self.request.GET.get("_code", "")

        if report == 'daily':
            before = date - relativedelta(days=1)
            after = date + relativedelta(days=1)
            interval = format(date, "d M Y")
            report_name = _("Daily")
        elif report == 'weekly':
            date = date - relativedelta(weekday=MO(-1))
            before = date - relativedelta(weeks=1)
            after = date + relativedelta(weeks=1)
            end = after - relativedelta(days=1)
            if date.month == end.month:
                interval = "%s - %s" % (format(date, "d"), format(end, "d M Y"))
            else:
                if date.year == end.year:
                    interval = "%s - %s" % (format(date, "d M"), format(end, "d M Y"))
                else:
                    interval = "%s - %s" % (format(date, "d M Y"), format(end, "d M Y"))
            report_name = _("Weekly")

        elif report == 'monthly':
            date = date - relativedelta(day=1)
            before = date - relativedelta(months=1)
            after = date + relativedelta(months=1)
            interval = format(date, "F, Y")
            report_name = _("Monthly")
        else:   # report == 'yearly':
            date = date - relativedelta(month=1, day=1)
            before = date - relativedelta(years=1)
            after = date + relativedelta(years=1)
            interval = format(date, "Y")
            report_name = _("Yearly")

        country = region = district = None

        if is_country_code(code):
            country = Country.objects.get(code=code).pk
        elif is_state_code(code):
            region = Region.objects.get(code=code).pk
        elif is_county_code(code):
            district = District.objects.get(code=code).pk

        context["country"] = country
        context["region"] = region
        context["district"] = district
        context["report"] = report
        context["report_name"] = report_name
        context["place"] = place
        context["today"] = today
        context["date"] = date
        context["before"] = before
        context["after"] = after
        context["interval"] = interval
        context["submissions"] = Checklist.objects.filter(date__gte=date, date__lt=after).count()
        context["reports"] = [
            ('daily', _("Daily")),
            ('weekly', _("Weekly")),
            ('monthly', _("Monthly")),
            ('yearly', _("Yearly")),
        ]

        return context


def autocomplete(request):
    data = []
    for code, place in Country.objects.all().values_list("code", "place"):
        data.append({
            "value": code,
            "label": place,
        })
    for code, place in Region.objects.all().values_list("code", "place"):
        data.append({
            "value": code,
            "label": place,
        })
    for code, place in District.objects.all().values_list("code", "place"):
        data.append({
            "value": code,
            "label": place,
        })
    return JsonResponse(data, safe=False)
