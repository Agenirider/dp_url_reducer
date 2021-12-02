"""
Django settings for url_reducer project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!bueb7%*g4bbuy#eyc-sm#d7r8a-w@52^89s%0t&k*8l=zq+d&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

if not DEBUG:
    sentry_sdk.init(
        dsn="https://6b1dcfb39fbc4c98b4397fc9645cefc6@o589561.ingest.sentry.io/6064961",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = [
        'domain1.link',
        'dom123.com',
        'test123.ru',
        'lalala.we',
        'blablabla.com',
        'api.redirect.link',
        'app.redirect.link'
    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions.backends.db',
    'rest_framework',
    'reducer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'url_reducer.urls'

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

WSGI_APPLICATION = 'url_reducer.wsgi.application'

REDIS_HOST = 'redis'
REDIS_PORT = 6379

if DEBUG:
    REDIS_HOST = 'localhost'

# CELERY SETTINGS
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/0'
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/0'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
    }
}

if not DEBUG:
    if 'DB_USER' in os.environ:
        DATABASES['default']['USER'] = os.environ.get('DB_USER')
        DATABASES['default']['PASSWORD'] = os.environ.get('DB_PASSWORD')
    if 'DB_HOST' in os.environ:
        DATABASES['default']['HOST'] = os.environ.get('DB_HOST')
    if 'DB_PORT' in os.environ:
        DATABASES['default']['PORT'] = os.environ.get('DB_PORT')
    if 'DB_ENGINE' in os.environ:
        DATABASES['default']["ENGINE"] = os.environ.get('DB_ENGINE')
    if 'DB_NAME' in os.environ:
        DATABASES['default']["NAME"] = os.environ.get('DB_NAME')

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

if not DEBUG:
    REDIS_HOST = 'redis'

# CORS BLOCK
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_METHODS = [
    'DELETE',
    'POST',
    'GET',
]
#
# CORS_ALLOW_HEADERS = [
#     'Access-Control-Allow-Headers',
#     'Access-Control-Allow-Credentials',
#     'accept',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
#     'x-ijt',
# ]
# #
CORS_ALLOWED_ORIGIN_REGEXES = [
    r'http://localhost',
    r"^http://redirect.link",
]

# if DEBUG:
#     # add jetbrains debugging headers (module JavaScript Debug)
#     from corsheaders.defaults import default_headers
#
#     CORS_ALLOW_HEADERS = default_headers + (
#         'x-ijt',
#    )

CORS_ALLOWED_ORIGINS = [
    "http://redirect.link",
    "http://app.redirect.link",
    "http://api.redirect.link",
    "http://domain1.link",
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = '/vol/web/static/'
MEDIA_ROOT = '/vol/web/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': os.path.join(BASE_DIR, 'url_reducer', 'debug.log')
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'file'],
            'propagate': True
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['console', 'file']
        }
    }
}
