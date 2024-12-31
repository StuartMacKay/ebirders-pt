from django.views.generic import TemplateView


class ChecklistsView(TemplateView):
    template_name = "checklists/index.html"
