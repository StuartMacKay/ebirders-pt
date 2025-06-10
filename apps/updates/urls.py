from django.urls import path

from .views import UpdatesView

app_name = "updates"

urlpatterns = [
    path("", UpdatesView.as_view(), name="list"),
]
