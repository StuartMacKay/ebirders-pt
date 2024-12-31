from django.urls import path

from .views import DigestView

app_name = "digest"

urlpatterns = [
    path("", DigestView.as_view(), name="index"),
]
