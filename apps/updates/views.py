from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.views import generic

from .models import Update


class UpdatesView(generic.ListView):
    model = Update
    template_name = "updates/list.html"
    ordering = "-published_at"
    queryset = Update.objects.published()
    paginate_by = 20

    @staticmethod
    def get_translations():
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("updates:list"), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["translations"] = self.get_translations()
        return context
