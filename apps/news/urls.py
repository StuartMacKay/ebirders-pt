from django.urls import path

from .views import LatestView, autocomplete

app_name = "news"

urlpatterns = [
    path("latest/", LatestView.as_view(), name="latest"),
    path("autocomplete/", autocomplete, name="autocomplete"),
]
