from checklists.models import Country, District, Location, Observer, Region, Species


def country_choices():
    return Country.objects.all().values_list("code", "name")


def country_choice(code):
    return (
        Country.objects.filter(code=code)
        .values_list("code", "name")
        .first()
    )


def state_choices(country_code):
    queryset = Region.objects.all()
    if country_code:
        queryset = queryset.filter(code__startswith=country_code)
    return queryset.values_list("code", "name")


def state_choice(code):
    return (
        Region.objects.filter(code=code)
        .values_list("code", "name")
        .first()
    )


def county_choices(country_code, state_code):
    queryset = District.objects.all()
    if state_code:
        queryset = queryset.filter(code__startswith=state_code)
    elif country_code:
        queryset = queryset.filter(code__stsartswith=country_code)
    return queryset.values_list("code", "name")


def county_choice(code):
    return (
        District.objects.filter(code=code)
        .values_list("code", "name")
        .first()
    )


def location_choices(country_code, state_code, county_code):
    queryset = Location.objects.all()
    if county_code:
        queryset = queryset.filter(district__code=county_code)
    elif state_code:
        queryset = queryset.filter(region__code=state_code)
    elif country_code:
        queryset = queryset.filter(country__code=country_code)
    return queryset.values_list("identifier", "name").distinct("identifier")


def location_choice(identifier):
    return (
        Location.objects.filter(identifier=identifier)
        .values_list("identifier", "name")
        .first()
    )


def observer_choices():
    queryset = Observer.objects.all().values_list("name", "name")
    return queryset.distinct("name")


def observer_choice(name):
    return Observer.objects.filter(name=name).values_list("name", "name").first()


def species_choices():
    return Species.objects.all().values_list("species_code", "common_name")


def species_choice(code):
    return (
        Species.objects.filter(species_code=code)
        .values_list("species_code", "common_name")
        .first()
    )
