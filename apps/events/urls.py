from django.urls import path

from .views import ModerationView

app_name = "events"

urlpatterns = [
    path("", ModerationView.as_view(), name="list"),
]
