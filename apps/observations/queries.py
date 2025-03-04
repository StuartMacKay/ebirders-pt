from ebird.checklists.models import Location, Observer, Species


def country_choices():
    queryset = Location.objects.all().values_list("country_code", "country")
    return queryset.distinct("country_code")


def country_choice(code):
    return Location.objects.filter(country_code=code).values_list("country_code", "country").first()


def state_choices(code):
    queryset = Location.objects.filter(country_code=code).values_list(
        "state_code", "state"
    )
    return queryset.distinct("state_code")


def state_choice(code):
    return Location.objects.filter(state_code=code).values_list("state_code", "state").first()


def county_choices(code):
    queryset = Location.objects.filter(state_code=code).values_list(
        "county_code", "county"
    )
    return queryset.distinct("county_code")


def county_choice(code):
    return Location.objects.filter(county_code=code).values_list("county_code", "county").first()


def location_choices(code):
    queryset = Location.objects.filter(county_code=code).values_list(
        "identifier", "name"
    )
    return queryset.distinct("identifier")


def location_choice(identifier):
    return Location.objects.filter(identifier=identifier).values_list("identifier", "name").first()


def observer_choices():
    queryset = Observer.objects.all().values_list(
        "name", "name"
    )
    return queryset.distinct("name")


def observer_choice(name):
    return Observer.objects.filter(name=name).values_list("name", "name").first()


def species_choices():
    return Species.objects.all().values_list(
        "species_code", "common_name"
    )


def species_choice(code):
    return Species.objects.filter(species_code=code).values_list("species_code", "common_name").first()
