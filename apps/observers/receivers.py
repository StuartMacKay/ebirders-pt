import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from data.models import Observer

logger = logging.getLogger(__name__)

# Normally there is a separator, |, -- between the name of the
# observer and any commercial name. In case the name is only the
# commercial name, check for the following keywords so the name
# can be reviewed and manually changed.
keywords = ["Tours", "Guide", "www", ".com"]


def remove_adverts(name):
    for separator in ["|", "--"]:
        if separator in name:
            name = name.split(separator, 1)[0].strip()
    return name


def remove_extra_spaces(name):
    if "  " in name:
        name = name.replace("  ", " ")
    return name


def flag_keywords(name):
    for keyword in keywords:
        if keyword in name:
            logger.warning("Review observer name: %s", name)


def generate_name(name) -> str:
    cleaned = remove_adverts(name)
    cleaned = remove_extra_spaces(cleaned)
    flag_keywords(cleaned)
    return cleaned


@receiver(pre_save, sender=Observer)
def set_observer_name(sender, instance, **kwargs):
    if instance.pk is None:
        instance.name = generate_name(instance.original)
