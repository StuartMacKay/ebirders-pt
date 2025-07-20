import json

from django.db.models import Q

from dal import autocomplete
from ebird.api.data.models import Country, County, Location, Observer, Species, State


class CountryList(autocomplete.Select2ListView):
    def get_list(self):
        return Country.objects.all().values_list("code", "name")


class StateList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = State.objects.all().values_list("code", "name")
        if countries := self.forwarded.get("country"):
            filters = Q()
            for country in countries:
                filters |= Q(code__startswith=country)
            queryset = queryset.filter(filters)
        return queryset


class CountyList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = County.objects.all().values_list("code", "name")
        if states := self.forwarded.get("state"):
            filters = Q()
            for state in states:
                filters |= Q(code__startswith=state)
            queryset = queryset.filter(filters)
        elif countries := self.forwarded.get("country"):
            filters = Q()
            for country in countries:
                filters |= Q(code__startswith=country)
            queryset = queryset.filter(filters)
        return queryset


class LocationList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = Location.objects.all().values_list("identifier", "name")
        if counties := self.forwarded.get("county"):
            queryset = queryset.filter(county__code__in=counties)
        elif states := self.forwarded.get("state"):
            queryset = queryset.filter(state__code__in=states)
        elif country := self.forwarded.get("country"):
            queryset = queryset.filter(country__code__in=country)
        return queryset


class ObserverList(autocomplete.Select2ListView):
    def get_list(self):
        return Observer.objects.all().values_list("identifier", "name")


class CommonNameList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = (
            Species.objects.all()
            .values_list("species_code", "common_name")
            .order_by("taxon_order")
        )
        return [
            ("%s" % code, json.loads(name)[self.request.LANGUAGE_CODE])
            for code, name in queryset
        ]


class ScientificNameList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = (
            Species.objects.all()
            .values_list("species_code", "scientific_name")
            .order_by("taxon_order")
        )
        return [(code, name) for code, name in queryset]


class FamilyList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = (
            Species.objects.all()
            .values_list("family_code", "family_scientific_name")
            .order_by("taxon_order")
        )
        return list({(code, name) for code, name in queryset})
