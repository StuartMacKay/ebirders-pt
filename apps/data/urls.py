from django.urls import path

from .views import (
    CountryAutocomplete,
    CountyAutocomplete,
    LocationAutocomplete,
    ObserverAutocomplete,
    SpeciesAutocomplete,
    StateAutocomplete,
)

app_name = "data"

urlpatterns = [
    path("countries/", CountryAutocomplete.as_view(), name="countries"),
    path("states/", StateAutocomplete.as_view(), name="states"),
    path("counties/", CountyAutocomplete.as_view(), name="counties"),
    path("locations/", LocationAutocomplete.as_view(), name="locations"),
    path("observers/", ObserverAutocomplete.as_view(), name="observers"),
    path("species", SpeciesAutocomplete.as_view(), name="species"),
]
