from django.views.generic import TemplateView


class DigestView(TemplateView):
    template_name = "digest/index.html"
