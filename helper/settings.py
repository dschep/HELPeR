import os
def envtuple(key, **opts):
    if key in os.environ:
        return (key, opts.get('convert', lambda x: x)(os.environ[key]))
    elif 'default' in opts:
        return (key, opts['default'])
    else:
        raise KeyError('{} not in os.environ'.format(key))

globals().update(dict([
    envtuple('SECRET_KEY'),
    envtuple('DEBUG', default=False, convert=lambda x: x.lower() == 'true'),
    envtuple('EMAIL_HOST', default='localhost'),
    envtuple('EMAIL_HOST_USER', default=''),
    envtuple('EMAIL_HOST_PASSWORD', default=''),
    envtuple('EMAIL_PORT', default=25, convert=int),
    envtuple('DEFAULT_FROM_EMAIL', default='root@localhost'),
    envtuple('SERVER_EMAIL', default='root@localhost'),
    envtuple('CELERY_SEND_TASK_ERROR_EMAILS', default=False, convert=lambda x: x.lower() == 'true'),
    envtuple('BROKER_URL'),
    envtuple('CELERY_RESULT_BACKEND', default=''),
]))

ADMINS = (('', os.environ.get('ADMIN_EMAIL', '')), )

import dj_database_url
DATABASES = {'default': dj_database_url.config()}


ALLOWED_HOSTS = ['*']


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'stronghold',
    'crispy_forms',
    'formtools',

    'helper',
    'helper.agents.facebook',
    'helper.agents.instagram',
    'helper.agents.pushbullet',
    'helper.agents.pushover',
    'helper.agents.github',
    'helper.agents.dropbox',
    'helper.agents.gmail',
    'helper.agents.email',
    'helper.agents.twitter',
    'helper.agents.wmata',
    'helper.agents.rss',
    'helper.agents.http',
    'helper.agents.test',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'stronghold.middleware.LoginRequiredMiddleware',
)

ROOT_URLCONF = 'helper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'helper.wsgi.application'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = 'static'


# don't redirect to HTTP when accessed via an HTTPS proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# don't barf on redirects cause of nginx
USE_X_FORWARDED_HOST = True


# custom celery scheduling
CELERYBEAT_LOOP_MAX_INTERVAL = 30
CELERYBEAT_SCHEDULER = 'helper.scheduler.TaskPairScheduler'


CRISPY_TEMPLATE_PACK = 'bootstrap3'
