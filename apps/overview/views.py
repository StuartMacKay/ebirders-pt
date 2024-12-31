from django.views.generic import TemplateView


class OverView(TemplateView):
    template_name = "overview/index.html"
