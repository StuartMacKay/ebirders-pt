from django.urls import path

from .views import SpeciesView

from .views import (
    CommonNameList,
    ScientificNameList
)

app_name = "species"

urlpatterns = [
    path("", SpeciesView.as_view(), name="list"),
    path("common-names", CommonNameList.as_view(), name="common-names"),
    path("scientific-names", ScientificNameList.as_view(), name="scientific-names"),
]
