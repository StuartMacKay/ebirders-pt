import datetime as dt
import logging
import random
import re
import socket
import string

from decimal import Decimal
from typing import List, Optional
from urllib.error import HTTPError, URLError

from django.db import transaction
from django.utils.timezone import get_default_timezone

import requests

from bs4 import BeautifulSoup
from ebird.api import get_checklist, get_regions, get_taxonomy, get_visits
from ebird.api.constants import API_MAX_RESULTS

from .models import (
    Checklist,
    Country,
    County,
    Location,
    Observation,
    Observer,
    Species,
    State,
)

logger = logging.getLogger(__name__)


def str2datetime(value: str) -> dt.datetime:
    return dt.datetime.fromisoformat(value).replace(tzinfo=get_default_timezone())


def random_word(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


class APILoader:
    """
    The APILoader downloads checklists from the eBird API and saves
    them to the database.

    Arguments:

        api_key: Your key to access the eBird API.
            Your can request a key at https://ebird.org/data/download.
            You will need an eBird account to do so.

        locale: The (default) locale used for species common names, etc.

        locales: A map of Django language codes to eBird locales so the species
                 common name, family name, etc. is displayed in the language
                 selected by the user.

        timeout: The timeout, in seconds, to use when connecting to the
                 eBird servers.

    The eBird API limits the number of records returned to 200. When downloading
    the visits for a given region if 200 hundred records are returned then it is
    assumed there are more and the loader will fetch the sub-regions and download
    the visits for each, repeating the process if necessary. To give an extreme
    example if you download the visits for the United States, "US", then the API
    will always return 200 results and the loader then download the visits to
    each of the 50 states and then each of the 3143 counties. DON'T TRY THIS
    AT HOME. Even if you don't get banned, if you melt the eBird servers, then
    karma will ensure bad things happen to you.

    Just occasionally, when fetching data from the eBird API, the connection will
    freeze and the APILoader will sit there doing nothing. The timeout will force
    the connection to be dropped, so you can try again. The APILoader does not
    retry making the connection. Connection freezes are sufficiently rare that
    it's not worth adding code to handle this, for now.

    """

    def __init__(self, api_key: str, locale: str, locales: dict, timeout: int = 30):
        self.api_key: str = api_key
        self.locale: str = locale
        self.locales: dict = locales
        socket.setdefaulttimeout(timeout)

    @staticmethod
    def get_country(data: dict) -> Country:
        code: str = data["countryCode"]
        values: dict = {
            "name": data["countryName"],
            "place": data["countryName"],
        }
        country, created = Country.objects.get_or_create(code=code, defaults=values)
        if created:
            logger.info("Added country: %s, %s", code, values["name"])
        return country

    @staticmethod
    def get_state(data: dict) -> State:
        code: str = data["subnational1Code"]
        values: dict = {
            "name": data["subnational1Name"],
            "place": "%s, %s" % (data["subnational1Name"], data["countryName"]),
        }
        state, created = State.objects.get_or_create(code=code, defaults=values)
        if created:
            logger.info("Added state: %s, %s", code, values["name"])
        return state

    @staticmethod
    def get_county(data) -> County:
        code: str = data["subnational2Code"]
        values: dict = {
            "name": data["subnational2Name"],
            "place": "%s, %s, %s"
            % (data["subnational2Name"], data["subnational1Name"], data["countryName"]),
        }
        county, created = County.objects.get_or_create(code=code, defaults=values)
        if created:
            logger.info("Added county: %s, %s", code, values["name"])
        return county

    def add_location(self, data: dict) -> Location:
        identifier: str = data["locId"]
        location: Location

        values: dict = {
            "identifier": identifier,
            "name": data["name"],
            "country": self.get_country(data),
            "state": self.get_state(data),
            "county": None,
            "hotspot": data["isHotspot"],
            "latitude": Decimal(data["latitude"]),
            "longitude": Decimal(data["longitude"]),
            "url": "https://ebird.org/region/%s" % identifier,
        }

        if "subnational2Code" in data:
            values["county"] = self.get_county(data)

        location = Location.objects.create(**values)
        logger.info("Added location: %s, %s", identifier, location.display_name())
        return location

    def add_species(self, code: str) -> Species:
        """
        Add the species with the eBird code.

        Arguments:
            code: the eBird code for the species, e.g. 'horlar' (Horned Lark).

        """
        data: dict = get_taxonomy(self.api_key, locale=self.locale, species=code)[0]

        values: dict = {
            "taxon_order": int(data["taxonOrder"]),
            "order": data.get("order", ""),
            "category": data["category"],
            "family_code": data.get("familyCode", ""),
            "common_name": data["comName"],
            "scientific_name": data["sciName"],
            "family_common_name": data.get("familyComName", ""),
            "family_scientific_name": data.get("familySciName", ""),
            "subspecies_common_name": "",
            "subspecies_scientific_name": "",
            "exotic_code": "",
            "data": {"common_name": {}},
        }

        species = Species(species_code=code, **values)

        for language, locale in self.locales.items():
            data = get_taxonomy(self.api_key, locale=locale, species=code)[0]
            species.data["common_name"][language] = data["comName"]

        species.save()

        logger.info("Added species: %s, %s", code, species.common_name)

        return species

    def get_species(self, data: dict) -> Species:
        code: str = data["speciesCode"]
        species = Species.objects.filter(species_code=code).first()
        if species is None:
            species = self.add_species(code)
        return species

    @staticmethod
    def get_urn(project_id, row: dict) -> str:
        return f"URN:CornellLabOfOrnithology:{project_id}:{row['obsId']}"

    def add_observation(self, data: dict, checklist: Checklist) -> Observation:
        identifier: str = data["obsId"]
        observation: Observation
        species: Species = self.get_species(data)

        values: dict = {
            "edited": checklist.edited,
            "identifier": identifier,
            "checklist": checklist,
            "country": checklist.country,
            "state": checklist.state,
            "county": checklist.county,
            "location": checklist.location,
            "observer": checklist.observer,
            "species": species,
            "date": checklist.date,
            "time": checklist.time,
            "started": checklist.started,
            "count": None,
            "media": False,
            "comments": "",
            "urn": self.get_urn(checklist.project_code, data),
        }

        if re.match(r"\d+", data["howManyStr"]):
            values["count"] = int(data["howManyStr"]) or None

        if "comments" in data:
            values["comments"] = data["comments"]

        observation, created = Observation.objects.get_or_create(
            identifier=identifier, defaults=values
        )

        return observation

    @staticmethod
    def get_observer_identifier(data) -> str:
        identifier: str = data["subId"]
        logger.info("Scraping checklist: %s", identifier)
        response = requests.get("https://ebird.org/checklist/%s" % identifier)
        content = response.content
        soup = BeautifulSoup(content, "lxml")
        attribute = "data-participant-userid"
        node = soup.find("span", attrs={attribute: True})
        return node[attribute] if node else ""

    def get_observer(self, data: dict) -> Observer:
        name: str = data.get("userDisplayName", "Anonymous eBirder")
        observer, created = Observer.objects.get_or_create(name=name)
        if observer.multiple:
            observer, created = Observer.objects.get_or_create(
                identifier=self.get_observer_identifier(data),
                defaults={
                    "name": random_word(8),
                    "byname": name
                }
            )
        elif observer.identifier == "":
            observer.identifier = self.get_observer_identifier(data)
            observer.save()
        if created:
            logger.info("Added observer: %s", observer.display_name())
        return observer

    def add_checklist(self, identifier: str) -> Checklist | None:
        """
        Add the checklist with the given identifier.

        Arguments:
            identifier: the eBird identifier for the checklist, e.g. "S318722167"

        """
        logger.info("Adding checklist: %s", identifier)

        with transaction.atomic():
            data: dict = get_checklist(self.api_key, identifier)
            identifier: str = data["subId"]
            created: dt.datetime = str2datetime(data["creationDt"])
            edited: dt.datetime = str2datetime(data["lastEditedDt"])
            started: dt.datetime = str2datetime(data["obsDt"])
            location: Location = Location.objects.get(identifier=data["locId"])
            checklist: Checklist
            observer: Observer = self.get_observer(data)

            if not observer.enabled:
                return None

            values: dict = {
                "created": created,
                "edited": edited,
                "country": location.country,
                "state": location.state,
                "county": location.county,
                "location": location,
                "observer": observer,
                "observer_count": None,
                "group": "",
                "species_count": data["numSpecies"],
                "date": started.date(),
                "time": None,
                "started": started,
                "protocol_code": data["protocolId"],
                "project_code": data["projId"],
                "duration": None,
                "complete": data["allObsReported"],
                "comments": "",
                "url": "https://ebird.org/checklist/%s" % identifier,
            }

            if data["obsTimeValid"]:
                values["time"] = started.time()

            if "numObservers" in data:
                values["observer_count"] = int(data["numObservers"])

            if duration := data.get("durationHrs"):
                values["duration"] = int(duration * 60.0)

            if data["protocolId"] == "P22":
                # The distance travelled might not be reported.
                if "effortDistanceKm" in data:
                    dist: str = data["effortDistanceKm"]
                    values["distance"] = round(Decimal(dist), 3)
            elif data["protocolId"] == "P23":
                coverage: str = data["effortAreaHa"]
                values["coverage"] = round(Decimal(coverage), 3)

            if "comments" in data:
                values["comments"] = data["comments"]

            checklist = Checklist.objects.create(identifier=identifier, **values)

            for observation_data in data["obs"]:
                self.add_observation(observation_data, checklist)

        return checklist

    def fetch_subregions(self, region: str) -> List[str]:
        region_types: list = ["subnational1", "subnational2", None]
        levels: int = len(region.split("-", 2))
        region_type: Optional[str] = region_types[levels - 1]

        if region_type:
            items: list = get_regions(self.api_key, region_type, region)
            sub_regions = [item["code"] for item in items]
        else:
            sub_regions = []

        return sub_regions

    def fetch_visits(self, region: str, date: dt.date):
        visits = []

        results: list = get_visits(
            self.api_key, region, date=date, max_results=API_MAX_RESULTS
        )

        if len(results) == API_MAX_RESULTS:
            logger.info("API result limit reached - fetching visits for subregions")
            if sub_regions := self.fetch_subregions(region):
                for sub_region in sub_regions:
                    logger.info("Fetching visits for sub-region: %s", sub_region)
                    visits.extend(self.fetch_visits(sub_region, date))
            else:
                # No more sub-regions, issue a warning and return the results
                visits.extend(results)
                logger.warning(
                    "Fetching visits - API limit reached: %s, %s", region, date
                )
        else:
            visits.extend(results)

        return visits

    def add_checklists(self, region: str, date: dt.date) -> None:
        """
        Add all the checklists submitted for a region for a given date.

        Arguments:
            region: The code for a national, subnational1, subnational2
                 area or hotspot identifier. For example, US, US-NY,
                 US-NY-109, or L1379126, respectively.

            date: The date the observations were made.

        """

        logger.info("Adding checklists: %s, %s", region, date)

        try:
            visits: list[dict] = self.fetch_visits(region, date)

            logger.info("Visits made: %d ", len(visits))

            for visit in visits:
                data = visit["loc"]
                identifier = data["locId"]
                if not Location.objects.filter(identifier=identifier).exists():
                    self.add_location(data)

            added: int = 0

            for visit in visits:
                identifier = visit["subId"]
                if not Checklist.objects.filter(identifier=identifier).exists():
                    self.add_checklist(identifier)
                    added += 1

            logger.info("Checklists added: %d ", added)
            logger.info("Adding checklists completed")

        except (URLError, HTTPError):
            logger.exception("Adding checklists failed: %s, %s", region, date)
