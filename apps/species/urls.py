from django.urls import path

from .views import YearlistView

app_name = "species"

urlpatterns = [
    path("yearlist/<int:year>/", YearlistView.as_view(), name="yearlist"),
]
