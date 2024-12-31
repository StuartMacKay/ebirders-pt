from django.urls import path

from .views import OverView

app_name = "overview"

urlpatterns = [
    path("", OverView.as_view(), name="index"),
]
