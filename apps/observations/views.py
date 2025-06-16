from django.conf import settings
from django.urls import reverse
from django.utils import translation

from django_filters.views import FilterView

from data.models import Country, Observation

from .filters import ObservationFilter


class ObservationsView(FilterView):
    model = Observation
    filterset_class = ObservationFilter
    template_name = "observations/list.html"
    paginate_by = 100
    ordering = ("-started",)

    def get_queryset(self):
        related = ["country", "state", "county", "location", "observer", "species"]
        queryset = super().get_queryset().select_related(*related)
        return self.filterset_class(self.request.GET, queryset).qs

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("observations:list"), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_country"] = Country.objects.all().count() > 1
        context["translations"] = self.get_translations()
        return context
