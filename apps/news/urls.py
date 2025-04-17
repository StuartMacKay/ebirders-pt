from django.urls import path

from .views import IndexView, autocomplete

app_name = "news"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("autocomplete/", autocomplete, name="autocomplete"),
]
