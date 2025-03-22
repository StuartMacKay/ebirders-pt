from dateutil.relativedelta import relativedelta

from django import template
from django.db import connection
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from checklists.models import Checklist

register = template.Library()


@register.inclusion_tag("dashboards/charts/checklist-species.html")
def checklist_species_chart(region, start, end):
    total = Checklist.objects.filter(date__gte=start, date__lt=end).count()
    with connection.cursor() as cursor:
        cursor.execute(
            f"select "
            f"count(*), "
            f"((species_count - 1) / 5)::int as quantile "
            f"from checklists_checklist "
            f"where date >= '{start}' "
            f"and date < '{end}' "
            f"and species_count > 0 "
            f"group by quantile"
        )
        result = sorted(cursor.fetchall(), key=lambda t: t[1])

        data: list[int] = []
        labels: list[str] = []

        for count, index in result:
            start = index * 5 + 1
            end = start + 4
            data.append(round((count * 100) / total, 1))
            labels.append("%d-%d" % (start, end))

    return {
        "xaxis_title": _("Number of species"),
        "yaxis_title": _("Percentage of checklists"),
        "label": _("Percentage"),
        "labels": labels,
        "data": data,
    }
