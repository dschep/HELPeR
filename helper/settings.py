import os
SECRET_KEY=os.environ.get('SECRET_KEY')

EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '25'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'false').lower() == 'true'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('SERVER_EMAIL')

ADMINS = (('', os.environ.get('ADMIN_EMAIL')), )

CELERY_SEND_TASK_ERROR_EMAILS = os.environ.get('EMAIL_USE_TLS', 'false').lower() == 'true'


DEBUG = False

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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'HOST': 'db',
        'USER': 'postgres',
    }
}


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
