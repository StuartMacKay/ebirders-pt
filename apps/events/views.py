from django.conf import settings
from django.urls import reverse
from django.utils import translation
from django.views.generic import ListView

from data.models import Event


class ModerationView(ListView):
    model = Event
    template_name = "events/list.html"
    paginate_by = 100
    queryset = Event.objects.all().select_related("observation")
    ordering = ("-created",)

    def get_translated_urls(self):
        urls = []
        for code, name in settings.LANGUAGES:
            with translation.override(code):
                urls.append((reverse("events:list"), name))
        return urls

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["translations"] = self.get_translated_urls()
        return context
