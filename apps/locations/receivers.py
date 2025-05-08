import re

from django.db.models.signals import pre_save
from django.dispatch import receiver

from data.models import Location

# +/- 90 degrees with comma or period for the decimal point,
# followed by 2-5 decimal places.
latitude_regex = r"-?\d{1,2}[.,]\d{2,5}"

# +/- 180 degrees with comma or period for the decimal point,
# followed by 2-5 decimal places.
longitude_regex = r"-?\d{1,3}[.,]\d{2,5}"

# Latitude and longitude, separated by comma, and/or optional space,
# surrounded by optional round brackets, and preceded with anm optional
# comma and a space. The initial part of the name is captured in a
# group for the next step. The word boundary is added since the .*
# is greedy, consume the comma, and so the match will fail.
coordinates_regex = r"^(.*)\b,? (:?\()?%s, ?%s(:?\))?$" % (latitude_regex, longitude_regex)

# Country code (hard-wired to PT). The initial part of the name
# is captured in a group for the next step.
country_regex = r"^(.*), PT$"

# Country code (hard-wired to PT), followed by the region name,
# which might be in any language. The initial part of the name
# is captured in a group for the next step.
region_regex = r"^(.*) PT-\w+$"


def remove_coordinates(name: str) -> str:
    if re.match(coordinates_regex, name):
        name = re.sub(coordinates_regex, r"\1", name)
    return name


def remove_country(name: str) -> str:
    if re.match(country_regex, name):
        name = re.sub(country_regex, r"\1", name)
    return name


def remove_region(name: str) -> str:
    if re.match(region_regex, name):
        name = re.sub(region_regex, r"\1", name)
    return name


def remove_state(name: str) -> str:
    """Remove the county or state.

    The location name, particularly for private locations is a comma
    separated list of the place, town and county. The latter might be
    the district (state) since counties, and districts are often named
    after the principal town or city.
    """
    elements = name.split(",")
    if len(elements) == 3:
        del elements[2]
        name = ",".join(elements)
    return name


def truncate(name: str) -> str:
    if len(name) > 80:
        name = name[:78] + "..."
    return name


def remove_duplicates(name: str) -> str:
    """The name of larger towns and cities is shared with the county
    or district so duplicate names are treated as the general area
    for the town or city."""
    elements = name.split(",")
    if len(elements) == 2 and elements[0] == elements[1]:
        name = "%s-área-geral" % elements[0]
    return name


def remove_access(name: str) -> str:
    if name.endswith(" (acesso condicionado)"):
        name = name.replace(" (acesso condicionado)", "")
    elif name.endswith(" - acesso condicionado"):
        name = name.replace(" - acesso condicionado", "")
    elif name.endswith(" (Acesso Condicionado)"):
        name = name.replace(" (Acesso Condicionado)", "")
    elif name.endswith(", Acesso Condicionado"):
        name = name.replace(", Acesso Condicionado", "")
    elif name.endswith("--Acesso Condicionado"):
        name = name.replace("--Acesso Condicionado", "")
    elif name.endswith(" (acesso restrito)"):
        name = name.replace(" (acesso restrito)", "")
    elif name.endswith(" (Acesso Restrito)"):
        name = name.replace(" (Acesso Restrito)", "")
    return name


def remove_freguesias(name):
    if "União das freguesias" in name:
        name = name.split(",")[0]
    return name


def generate_byname(name) -> str:
    cleaned = remove_coordinates(name)
    cleaned = remove_country(cleaned)
    cleaned = remove_region(cleaned)
    cleaned = remove_state(cleaned)
    cleaned = remove_access(cleaned)
    cleaned = remove_freguesias(cleaned)
    cleaned = remove_duplicates(cleaned)
    cleaned = truncate(cleaned)
    return cleaned if cleaned != name else ""


@receiver(pre_save, sender=Location)
def set_location_byname(sender, instance, **kwargs):
    if instance.pk is None:
        instance.byname = generate_byname(instance.name)
