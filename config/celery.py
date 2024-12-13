import os

from celery import Celery  # type: ignore
from celery.signals import setup_logging  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery()


class CeleryConfig:
    # Configure logging using Django's LOGGING setting. Caveat: since logging
    # is configured using the setup_logging signal, see below, this might not
    # be needed.
    worker_hijack_root_logger = False

    # The default, unless it is overridden using an environment variable
    # is to assume we are running the demo using a virtualenv and connect
    # to a locally install instance of rabbitmq. When using containers,
    # the broker url will be set to connect to the rabbitmq service.
    broker_url = os.environ.get(
        "BROKER_URL", "amqp://guest:guest@localhost:5672/project"
    )


# Load the configuration
app.config_from_object(CeleryConfig)
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {}


@setup_logging.connect
def receiver_setup_logging(loglevel, logfile, format, colorize, **kwargs):  # noqa
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)
