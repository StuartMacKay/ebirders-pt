from dal import autocomplete
from ebird.api.data.models import Observer


class ObserverList(autocomplete.Select2ListView):
    def get_list(self):
        return Observer.objects.all().values_list("identifier", "name")
