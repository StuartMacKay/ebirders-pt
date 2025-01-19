from django.urls import path

from .views import ChecklistsView, CountryAutocomplete, StateAutocomplete, CountyAutocomplete

app_name = "checklists"

urlpatterns = [
    path("", ChecklistsView.as_view(), name="list"),
    path("countries/", CountryAutocomplete.as_view(), name="countries"),
    path("states/", StateAutocomplete.as_view(), name="states"),
    path("counties/", CountyAutocomplete.as_view(), name="counties"),
]
