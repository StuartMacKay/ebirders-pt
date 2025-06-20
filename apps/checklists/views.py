from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property
from django.views import generic

from checklists.forms import ChecklistFilterForm
from data.models import Checklist, Country


class ChecklistsView(generic.edit.FormMixin, generic.ListView):
    form_class = ChecklistFilterForm
    model = Checklist
    ordering = ("-started",)
    paginate_by = 50
    template_name = "checklists/list.html"

    @cached_property
    def show_country(self):
        return Country.objects.all().count() > 1

    def get_filters(self):
        filters = Q()
        if country := self.request.GET.get("country"):
            filters &= Q(country__code=country)
        if state := self.request.GET.get("state"):
            filters &= Q(state__code=state)
        if county := self.request.GET.get("county"):
            filters &= Q(county__code=county)
        if location := self.request.GET.get("location"):
            filters &= Q(location__identifier=location)
        if observer := self.request.GET.get("observer"):
            filters &= Q(observer__identifier=observer)
        if start := self.request.GET.get("start"):
            filters &= Q(date__gte=start)
        if finish := self.request.GET.get("finish"):
            filters &= Q(date__lte=finish)
        if hotspot := self.request.GET.get("hotspot"):
            filters &= Q(location__hotspot=hotspot)
        return filters

    def get_ordering(self):
        if order := self.request.GET.get("order"):
            ordering = (order,)
        else:
            ordering = super().get_ordering()
        return ordering

    def get_related(self):  # noqa
        return ["country", "state", "county", "location", "observer"]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(self.get_filters())
        return queryset.select_related(*self.get_related())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["data"] = self.request.GET
        kwargs["show_country"] = self.show_country
        return kwargs

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.is_valid()
        return form

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("checklists:list"), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
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
