from django.urls import path

from .views import eBirdersView

app_name = "ebirders"

urlpatterns = [
    path("", eBirdersView.as_view(), name="index"),
]
