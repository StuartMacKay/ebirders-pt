import json

from django.db.models import Q
from django.views import generic

from dal import autocomplete

from data.models import Country, County, Location, Observer, Species, State


class FilteredListView(generic.ListView):
    form_classes = None
    related = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object_list = None
        self.forms = []

    def get_related(self):
        return self.related

    def get_ordering(self):
        ordering = []
        for form in self.forms:
            ordering.extend(form.get_ordering())
        return ordering

    def get_filters(self):
        filters = Q(published=True)
        for form in self.forms:
            filters &= form.get_filters()
        return filters

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(self.get_filters())
        queryset = queryset.select_related(*self.get_related())
        return queryset

    def get_forms(self, form_class=None):
        forms = [klass(data=self.request.GET) for klass in self.form_classes]
        for form in forms:
            form.is_valid()
        return forms

    def get(self, request, *args, **kwargs):
        self.forms = self.get_forms()
        self.object_list = self.get_queryset()
        context = self.get_context_data(forms=self.forms)
        return self.render_to_response(context)


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
        queryset = Location.objects.all().values_list("identifier", "byname")
        if counties := self.forwarded.get("county"):
            filters = Q()
            for county in counties:
                filters |= Q(county__code__startswith=county)
            queryset = queryset.filter(filters)
        return queryset


class ObserverAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return Observer.objects.all().values_list("identifier", "byname")


class SpeciesAutocomplete(autocomplete.Select2ListView):
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
