from django.urls import path

from .views import ObserverList

app_name = "observers"

urlpatterns = [
    path("observers/", ObserverList.as_view(), name="observers"),
]
