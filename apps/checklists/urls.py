from django.urls import path, re_path

from .views import DetailView, ChecklistsView, CountryAutocomplete, StateAutocomplete, CountyAutocomplete, LocationAutocomplete

app_name = "checklists"

urlpatterns = [
    path("", ChecklistsView.as_view(), name="list"),
    re_path(r"^(?P<identifier>S\d+)/$", DetailView.as_view(), name="detail"),
    path("countries/", CountryAutocomplete.as_view(), name="countries"),
    path("states/", StateAutocomplete.as_view(), name="states"),
    path("counties/", CountyAutocomplete.as_view(), name="counties"),
    path("locations/", LocationAutocomplete.as_view(), name="locations"),
]
