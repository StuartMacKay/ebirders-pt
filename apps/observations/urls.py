from django.urls import path

from .views import autocomplete, ObservationsView

app_name = "observations"

urlpatterns = [
    path("", ObservationsView.as_view(), name="list"),
    path("autocomplete/", autocomplete, name="autocomplete"),
]
