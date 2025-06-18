from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property
from django.views import generic

from django_filters.views import FilterView

from data.models import Checklist, Country

from .filters import ChecklistFilter


class ChecklistsView(FilterView):
    model = Checklist
    filterset_class = ChecklistFilter
    template_name = "checklists/list.html"
    paginate_by = 50
    ordering = ("-started",)

    @cached_property
    def show_country(self):
        return Country.objects.all().count() > 1

    def get_queryset(self):
        related = ["country", "state", "county", "location", "observer"]
        return super().get_queryset().select_related(*related)

    def get_filterset(self, filterset_class):
        kwargs = self.get_filterset_kwargs(filterset_class)
        kwargs["show_country"] = self.show_country
        return filterset_class(**kwargs)

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("checklists:list"), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_country"] = self.show_country
        context["translations"] = self.get_translations()
        return context


class DetailView(generic.DetailView):
    model = Checklist
    template_name = "checklists/detail.html"
    context_object_name = "checklist"

    def get_object(self, queryset=None):
        return get_object_or_404(Checklist, identifier=self.kwargs["identifier"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["observations"] = context["checklist"].observations.all()
        return context
