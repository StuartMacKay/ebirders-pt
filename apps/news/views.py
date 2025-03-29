import datetime as dt
import re

from dateutil.relativedelta import relativedelta, MO
from django.http import JsonResponse
from django.utils import timezone
from django.utils.dateformat import format
from django.utils.translation import gettext_lazy as _
from django.views import generic
from ebird.codes.locations import is_country_code, is_state_code, is_county_code

from checklists.models import Checklist, Country, District, Region


class IndexView(generic.TemplateView):
    template_name = "news/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        week = self.request.GET.get("week", "")
        code = self.request.GET.get("code", "")
        place = self.request.GET.get("_code", "")

        if week:
            week_start = dt.datetime.strptime("%s-1" % week, "%Y-%W-%w").date()
        else:
            week_start = timezone.now().date() - relativedelta(weekday=MO(-1))

        week_end = week_start + relativedelta(days=6)

        if week_start.month == week_end.month:
            subtitle = "%s - %s" % (format(week_start, "d"), format(week_end, "d M Y"))
        else:
            if week_start.year == week_end.year:
                subtitle = "%s - %s" % (
                    format(week_start, "d M"),
                    format(week_end, "d M Y"),
                )
            else:
                subtitle = "%s - %s" % (
                    format(week_start, "d M Y"),
                    format(week_end, "d M Y"),
                )

        last_week = week_start - relativedelta(days=1)
        next_week = week_start + relativedelta(days=7)

        country = region = district = None

        if is_country_code(code):
            country = Country.objects.get(code=code).pk
        elif is_state_code(code):
            region = Region.objects.get(code=code).pk
        elif is_county_code(code):
            district = District.objects.get(code=code).pk

        if Country.objects.all().count() == 1:
            autocomplete_placeholder = _("Enter Region or County")
        else:
            autocomplete_placeholder = _("Enter Country, Region or County")

        context["country"] = country
        context["region"] = region
        context["district"] = district
        context["place"] = place
        context["week_start"] = week_start
        context["week_end"] = week_end + relativedelta(days=1)
        context["this_week"] = week_start.strftime("%Y-%W")
        context["last_week"] = last_week.strftime("%Y-%W")
        context["next_week"] = next_week.strftime("%Y-%W")
        context["subtitle"] = subtitle
        context["autocomplete_placeholder"] = autocomplete_placeholder
        context["submissions"] = Checklist.objects.filter(
            date__gte=week_start, date__lte=week_end
        ).count()

        return context


def autocomplete(request):
    """
    Return the list of countries, regions and districts for the search
    field. If there is only one country, remove it from the label.
    """
    data = []

    for code, place in Country.objects.all().values_list("code", "place"):
        data.append(
            {
                "value": code,
                "label": place,
            }
        )

    if len(data) == 1:
        country = data.pop(0)["label"]
    else:
        country = None

    for code, place in Region.objects.all().values_list("code", "place"):
        if country:
            label = re.sub(r", %s$" % country, "", place)
        else:
            label = place
        data.append({"value": code, "label": label})

    for code, place in District.objects.all().values_list("code", "place"):
        if country:
            label = re.sub(r", %s$" % country, "", place)
        else:
            label = place
        data.append({"value": code, "label": label})

    return JsonResponse(data, safe=False)
