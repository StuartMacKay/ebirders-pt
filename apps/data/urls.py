from django.urls import path

from .autocompletes import (
    CommonNameList,
    CountryList,
    CountyList,
    LocationList,
    ObserverList,
    ScientificNameList,
    StateList,
)

app_name = "data"

urlpatterns = [
    path("countries/", CountryList.as_view(), name="countries"),
    path("states/", StateList.as_view(), name="states"),
    path("counties/", CountyList.as_view(), name="counties"),
    path("locations/", LocationList.as_view(), name="locations"),
    path("observers/", ObserverList.as_view(), name="observers"),
    path("common-name", CommonNameList.as_view(), name="common-name"),
    path("scientific-name", ScientificNameList.as_view(), name="scientific-name"),
]
