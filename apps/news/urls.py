from django.urls import path
from django.views.decorators.cache import cache_page

from .views import NewsView

app_name = "news"

# Cache expiration intervals
minutes: int = 60
hours: int = 60 * minutes
days: int = 24 * hours

urlpatterns = [
    path("", cache_page(1 * hours)(NewsView.as_view()), name="index"),
]
