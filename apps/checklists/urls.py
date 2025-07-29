from django.urls import path

from .views import ChecklistsView

app_name = "checklists"

urlpatterns = [
    path("", ChecklistsView.as_view(), name="list"),
]
