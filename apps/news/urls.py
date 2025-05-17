from django.urls import path

from .views import LatestView, WeeklyView, autocomplete

app_name = "news"

urlpatterns = [
    path("latest/", LatestView.as_view(), name="latest"),
    path("weekly/", WeeklyView.as_view(), name="weekly"),
    path("weekly/<int:year>/<int:week>/", WeeklyView.as_view(), name="for-week"),
    path("autocomplete/", autocomplete, name="autocomplete"),
]
