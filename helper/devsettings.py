from .settings import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.messages',
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda x: True}
