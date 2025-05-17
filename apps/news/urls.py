from django.urls import path

from .views import LatestView, MonthlyView, WeeklyView, autocomplete

app_name = "news"

urlpatterns = [
    path("latest/", LatestView.as_view(), name="latest"),
    path("weekly/", WeeklyView.as_view(), name="weekly"),
    path("weekly/<int:year>/<int:week>/", WeeklyView.as_view(), name="for-week"),
    path("monthly/", MonthlyView.as_view(), name="monthly"),
    path("monthly/<int:year>/<int:month>/", MonthlyView.as_view(), name="for-month"),
    path("autocomplete/", autocomplete, name="autocomplete"),
]
