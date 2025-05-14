from dal import autocomplete

from data.models import Country, County, Location, Observer, State


class CountryAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return Country.objects.all().values_list("code", "name")


class StateAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        queryset = State.objects.all().values_list("code", "name")
        if country := self.forwarded.get("country"):
            queryset = queryset.filter(code__startswith=country)
        return queryset


class CountyAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        queryset = County.objects.all().values_list("code", "name")
        if state := self.forwarded.get("state"):
            queryset = queryset.filter(code__startswith=state)
        return queryset


class LocationAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        queryset = Location.objects.all().values_list("identifier", "name")
        if county := self.forwarded.get("county"):
            queryset = queryset.filter(county__code=county)
        return queryset


class ObserverAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return Observer.objects.all().values_list("identifier", "name")
