from dal import autocomplete
import datetime as dt

from dateutil.relativedelta import relativedelta, MO

from django.utils import timezone
from django.utils.dateformat import format
from django.utils.translation import gettext_lazy as _
from django.views import generic

from checklists.models import Checklist


class IndexView(generic.TemplateView):
    template_name = "dashboards/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if date_str := self.request.GET.get("date"):
            date = dt.datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            date = timezone.now().date()

        report = self.request.GET.get("report", "daily")

        if report == 'daily':
            before = date - relativedelta(days=1)
            after = date + relativedelta(days=1)
            interval = format(date, "d M Y")
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

        elif report == 'monthly':
            date = date - relativedelta(day=1)
            before = date - relativedelta(months=1)
            after = date + relativedelta(months=1)
            interval = format(date, "F, Y")
        else:   # report == 'yearly':
            date = date - relativedelta(month=1, day=1)
            before = date - relativedelta(years=1)
            after = date + relativedelta(years=1)
            interval = format(date, "Y")

        context["report"] = self.request.GET.get("report", "daily")
        context["today"] = timezone.now().date()
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
