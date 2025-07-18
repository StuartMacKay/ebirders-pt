from django.urls import path

from .views import SpeciesView

app_name = "species"

urlpatterns = [
    path("", SpeciesView.as_view(), name="list"),
]
