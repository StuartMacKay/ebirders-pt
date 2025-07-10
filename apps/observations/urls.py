from django.urls import path
from django.views.decorators.cache import cache_page

from .views import ObservationsView

# Cache expiration intervals
minutes: int = 60
hours: int = 60 * minutes
days: int = 24 * hours

app_name = "observations"

urlpatterns = [
    path("", cache_page(1 * hours)(ObservationsView.as_view()), name="list"),
]
