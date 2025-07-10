from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views import ChecklistsView

# Cache expiration intervals
minutes: int = 60
hours: int = 60 * minutes
days: int = 24 * hours

app_name = "checklists"

urlpatterns = [
    path("", cache_page(1 * hours)(ChecklistsView.as_view()), name="list"),
]
