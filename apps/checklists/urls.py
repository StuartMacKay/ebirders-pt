from django.urls import path, re_path

from .views import (
    autocomplete,
    DetailView,
    ChecklistsView,
)

app_name = "checklists"

urlpatterns = [
    path("", ChecklistsView.as_view(), name="list"),
    path("autocomplete/", autocomplete, name="autocomplete"),
    re_path(r"^(?P<identifier>S\d+)/$", DetailView.as_view(), name="detail"),
]
