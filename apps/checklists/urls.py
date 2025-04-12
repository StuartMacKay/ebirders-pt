from django.urls import path, re_path

from .views import (
    DetailView,
    ChecklistsView,
    CountryAutocomplete,
    DistrictAutocomplete,
    CountyAutocomplete,
    LocationAutocomplete,
    ObserverAutocomplete,
)

app_name = "checklists"

urlpatterns = [
    path("", ChecklistsView.as_view(), name="list"),
    re_path(r"^(?P<identifier>S\d+)/$", DetailView.as_view(), name="detail"),
    path("countries/", CountryAutocomplete.as_view(), name="countries"),
    path("districts/", DistrictAutocomplete.as_view(), name="districts"),
    path("counties/", CountyAutocomplete.as_view(), name="counties"),
    path("locations/", LocationAutocomplete.as_view(), name="locations"),
    path("observers/", ObserverAutocomplete.as_view(), name="observers"),
]
