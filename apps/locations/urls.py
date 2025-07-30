from django.urls import path

from .views import CountryList, CountyList, LocationList, StateList

app_name = "locations"

urlpatterns = [
    path("countries/", CountryList.as_view(), name="countries"),
    path("states/", StateList.as_view(), name="states"),
    path("counties/", CountyList.as_view(), name="counties"),
    path("locations/", LocationList.as_view(), name="locations"),
]
