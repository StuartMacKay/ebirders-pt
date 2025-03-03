from ebird.checklists.models import Location


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
