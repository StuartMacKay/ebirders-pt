from django.urls import path
from django.views.decorators.cache import cache_page

from .views import LatestView, MonthlyView, WeeklyView, autocomplete

app_name = "news"

# Cache expiration intervals
minutes: int = 60
hours: int = 60 * minutes
days: int = 24 * hours

urlpatterns = [
    path(
        "latest/",
        cache_page(1 * hours)(LatestView.as_view()),
        name="latest",
    ),
    path(
        "weekly/",
        cache_page(1 * hours)(WeeklyView.as_view()),
        name="weekly",
    ),
    path(
        "weekly/<int:year>/<int:week>/",
        cache_page(1 * hours)(WeeklyView.as_view()),
        name="for-week",
    ),
    path(
        "monthly/",
        cache_page(1 * hours)(MonthlyView.as_view()),
        name="monthly",
    ),
    path(
        "monthly/<int:year>/<int:month>/",
        cache_page(1 * hours)(MonthlyView.as_view()),
        name="for-month",
    ),
    path(
        "autocomplete/",
        cache_page(1 * hours)(autocomplete),
        name="autocomplete",
    ),
]
