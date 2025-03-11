from dateutil.relativedelta import relativedelta

from django.views import generic
from django.utils import timezone
from ebird.checklists.models import Checklist



class IndexView(generic.TemplateView):
    template_name = "dashboards/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        one_week_ago = today - relativedelta(days=7)
        checklists = Checklist.objects.filter(date__gt=one_week_ago).order_by('-species_count')[:10]
        context["checklists"] = sorted(list(checklists), key=lambda checklist: checklist.started)
        return context
