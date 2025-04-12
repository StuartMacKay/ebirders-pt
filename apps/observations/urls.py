from django.urls import path

from .views import (
    ObservationsView,
    CountryAutocomplete,
    DistrictAutocomplete,
    CountyAutocomplete,
    LocationAutocomplete,
    ObserverAutocomplete,
    SpeciesAutocomplete,
)

app_name = "observations"

urlpatterns = [
    path("", ObservationsView.as_view(), name="list"),
    path("countries/", CountryAutocomplete.as_view(), name="countries"),
    path("districts/", DistrictAutocomplete.as_view(), name="districts"),
    path("counties/", CountyAutocomplete.as_view(), name="counties"),
    path("locations/", LocationAutocomplete.as_view(), name="locations"),
    path("observers/", ObserverAutocomplete.as_view(), name="observers"),
    path("species/", SpeciesAutocomplete.as_view(), name="species"),
]
