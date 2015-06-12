from .settings import *

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.messages',
)

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
)
