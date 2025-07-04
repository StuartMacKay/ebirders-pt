import json

from django.db.models import Q

from dal import autocomplete

from data.models import Country, County, Location, Observer, Species, State


class CountryList(autocomplete.Select2ListView):
    def get_list(self):
        return Country.objects.all().values_list("code", "name")


class StateList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = State.objects.all().values_list("code", "name")
        if countries := self.forwarded.get("country"):
            queryset = queryset.filter(code__in=countries)
        return queryset


class CountyList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = County.objects.all().values_list("code", "name")
        if states := self.forwarded.get("state"):
            filters = Q()
            for state in states:
                filters |= Q(code__startswith=state)
            queryset = queryset.filter(filters)
        elif country := self.forwarded.get("country"):
            queryset = queryset.filter(code__startswith=country)
        return queryset


class LocationList(autocomplete.Select2ListView):
    def get_list(self):
        queryset = Location.objects.all().values_list("identifier", "byname")
        if counties := self.forwarded.get("county"):
            queryset = queryset.filter(county__code__in=counties)
        elif states := self.forwarded.get("state"):
            queryset = queryset.filter(state__code__in=states)
        elif country := self.forwarded.get("country"):
            queryset = queryset.filter(country__code=country)
        return queryset


class ObserverList(autocomplete.Select2ListView):
    def get_list(self):
        return Observer.objects.all().values_list("identifier", "byname")


class SpeciesList(autocomplete.Select2ListView):
    # The autocomplete for species includes the common name in the currently
    # selected language, along with the scientific name. The filter uses the
    # species code, so the list of values contains an entry for common name
    # and an entry for the scientific name, with the same species code. The
    # problem is that when a selection is made and the page is redisplayed
    # the first entry in the list with the chosen species code is shown, for
    # instance, the common name, even though the scientific name was selected.
    # To get around this a single character prefix, '_' is added to the code
    # for the entries of scientific names, so the correct species name can
    # be displayed.

    def get_list(self):
        queryset = (
            Species.objects.all()
            .values_list("species_code", "common_name")
            .order_by("taxon_order")
        )
        common_names = [
            ("%s" % code, json.loads(name)[self.request.LANGUAGE_CODE])
            for code, name in queryset
        ]

        queryset = (
            Species.objects.all()
            .values_list("species_code", "scientific_name")
            .order_by("taxon_order")
        )
        scientific_names = [("_%s" % code, name) for code, name in queryset]

        # Return the list showing the species common name followed by the
        # scientific name.
        return [
            val
            for pair in zip(list(common_names), list(scientific_names))
            for val in pair
        ]
