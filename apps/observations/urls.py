from django.urls import path

from .views import BigDayView, ObservationsView, autocomplete

app_name = "observations"

urlpatterns = [
    path("", ObservationsView.as_view(), name="list"),
    path("big-day/", BigDayView.as_view(), name="big-day"),
    path("autocomplete/", autocomplete, name="autocomplete"),
]
