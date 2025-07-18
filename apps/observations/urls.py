from django.urls import path

from .views import ObservationsView

app_name = "observations"

urlpatterns = [
    path("", ObservationsView.as_view(), name="list"),
]
