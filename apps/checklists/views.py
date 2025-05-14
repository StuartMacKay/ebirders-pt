from django.views import generic

from django_filters.views import FilterView

from data.models import Checklist, Country

from .filters import ChecklistFilter


class ChecklistsView(FilterView):
    model = Checklist
    filterset_class = ChecklistFilter
    template_name = "checklists/index.html"
    paginate_by = 50
    ordering = ("-started",)

    def get_queryset(self):
        related = ["country", "state", "county", "location", "observer"]
        queryset = super().get_queryset().select_related(*related)
        return self.filterset_class(self.request.GET, queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_country"] = Country.objects.all().count() > 1
        return context


class DetailView(generic.DetailView):
    model = Checklist
    template_name = "checklists/detail.html"
    context_object_name = "checklist"

    def get_object(self, queryset=None):
        return Checklist.objects.get(identifier=self.kwargs["identifier"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["observations"] = context["checklist"].observations.all()
        return context
