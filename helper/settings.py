SECRET_KEY = 'lt#2nl*x^ib*emo^hwq8k5ztzzf@3e)y7--1s)^_b=@yf&ag)@'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.postgres',

    'stronghold',
    'tastypie',
    'crispy_forms',

    'helper',
    'helper.agents.facebook',
    'helper.agents.instagram',
    'helper.agents.pushbullet',
    'helper.agents.github',
    'helper.agents.dropbox',
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
        'NAME': 'helper',
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'


# don't redirect to HTTP when accessed via an HTTPS proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# custom celery scheduling
CELERYBEAT_LOOP_MAX_INTERVAL = 30
CELERYBEAT_SCHEDULER = 'helper.scheduler.TaskPairScheduler'


CRISPY_TEMPLATE_PACK = 'bootstrap3'
