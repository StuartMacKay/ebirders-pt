from django.urls import path, re_path

from .views import (
    ChecklistsView,
    DetailView,
)

app_name = "checklists"

urlpatterns = [
    path("", ChecklistsView.as_view(), name="list"),
    re_path(r"^(?P<identifier>S\d+)/$", DetailView.as_view(), name="detail"),
]
