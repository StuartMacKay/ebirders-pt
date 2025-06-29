from django.urls import path
from django.views.decorators.cache import cache_page

from .views import SpeciesView

# Cache expiration intervals
minutes: int = 60
hours: int = 60 * minutes
days: int = 24 * hours

app_name = "species"

urlpatterns = [
    path("", cache_page(1 * hours)(SpeciesView.as_view()), name="list"),
]
