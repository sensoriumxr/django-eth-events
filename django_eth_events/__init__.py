import django
from .apps import app as celery_app

if django.VERSION < (3, 2):
    default_app_config = 'django_eth_events.apps.DjangoEthEventsConfig'

__all__ = ['celery_app']
