from django.urls import path

from .views import BigDayView, ObservationsView

app_name = "observations"

urlpatterns = [
    path("", ObservationsView.as_view(), name="list"),
    path("big-day/", BigDayView.as_view(), name="big-day"),
]
