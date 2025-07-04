from django.urls import path

from .autocompletes import (
    CountryList,
    CountyList,
    LocationList,
    ObserverList,
    SpeciesList,
    StateList,
)

app_name = "data"

urlpatterns = [
    path("countries/", CountryList.as_view(), name="countries"),
    path("states/", StateList.as_view(), name="states"),
    path("counties/", CountyList.as_view(), name="counties"),
    path("locations/", LocationList.as_view(), name="locations"),
    path("observers/", ObserverList.as_view(), name="observers"),
    path("species", SpeciesList.as_view(), name="species"),
]
