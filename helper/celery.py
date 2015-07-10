import os

from celery import Celery

from django.conf import settings

app = Celery('helper', broker='redis://broker', backend='redis://broker')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
