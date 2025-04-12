from checklists.models import Country, County, District, Location, Observer, Species


def country_choices():
    return Country.objects.all().values_list("code", "name")


def country_choice(code):
    return (
        Country.objects.filter(code=code)
        .values_list("code", "name")
        .first()
    )


def district_choices(country_code):
    queryset = District.objects.all()
    if country_code:
        queryset = queryset.filter(code__startswith=country_code)
    return queryset.values_list("code", "name")


def district_choice(code):
    return (
        District.objects.filter(code=code)
        .values_list("code", "name")
        .first()
    )


def county_choices(country_code, district_code):
    queryset = County.objects.all()
    if district_code:
        queryset = queryset.filter(code__startswith=district_code)
    elif country_code:
        queryset = queryset.filter(code__startswith=country_code)
    return queryset.values_list("code", "name")


def county_choice(code):
    return (
        County.objects.filter(code=code)
        .values_list("code", "name")
        .first()
    )


def location_choices(country_code, district_code, county_code):
    queryset = Location.objects.all()
    if county_code:
        queryset = queryset.filter(county__code=county_code)
    elif district_code:
        queryset = queryset.filter(district__code=district_code)
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
