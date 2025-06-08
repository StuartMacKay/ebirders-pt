from django.urls import path

from .views import SpeciesView, YearlistView

app_name = "species"

urlpatterns = [
    path("", SpeciesView.as_view(), name="list"),
    path("yearlist/<int:year>/", YearlistView.as_view(), name="yearlist"),
]
