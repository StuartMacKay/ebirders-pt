from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import translation
from django.utils.functional import cached_property
from django.views import generic

from checklists.forms import ChecklistFilterForm
from data.models import Checklist, Country


class ChecklistsView(generic.list.MultipleObjectMixin, generic.FormView):
    form_class = ChecklistFilterForm
    model = Checklist
    paginate_by = 50
    template_name = "checklists/list.html"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form = None

    @cached_property
    def show_country(self):
        return Country.objects.all().count() > 1

    def get_ordering(self):
        return self.form.get_ordering()

    def get_related(self):  # noqa
        return ["country", "state", "county", "location", "observer"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if filters := self.form.get_filters():
            queryset = queryset.filter(filters)
        if related := self.get_related():
            queryset = queryset.select_related(*related)
        return queryset

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
        context["show_country"] = self.show_country
        context["translations"] = self.get_translations()
        return context

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        objects = self.get_queryset()
        context = self.get_context_data(object_list=objects, form=self.form)
        return self.render_to_response(context)


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
