import random
import string

from factory import Faker, LazyAttribute
from factory.django import DjangoModelFactory

from data.models import Observer


def random_code(length: int, prefix: str = ""):
    return prefix + "".join(random.choices(string.digits, k=length))


class ObserverFactory(DjangoModelFactory):
    class Meta:
        model = Observer
        django_get_or_create = ("name",)

    identifier = LazyAttribute(lambda _: random_code(7, "USER"))
    name = Faker("name")
