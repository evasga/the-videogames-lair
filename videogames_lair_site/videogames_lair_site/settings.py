"""
Django settings for videogames_lair_site project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sensitive settings are hidden
secrets_file = os.path.join(BASE_DIR, "secrets.json")
secrets = None
if os.path.isfile(secrets_file):
    with open(secrets_file) as f:
        secrets = json.load(f)


def get_secret(setting: str, is_list: bool = False, optional: bool = False):
    try:
        if secrets:
            return secrets[setting]
        elif is_list:
            return json.loads(os.environ[setting])
        else:
            return os.environ[setting]
    except KeyError:
        if optional:
            return None
        else:
            raise ImproperlyConfigured("Set the '{}' setting".format(setting))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", ".videogameslair.com"]


# Application definition

INSTALLED_APPS = [
    'vgl.apps.VglConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.steam',
    'sequences.apps.SequencesConfig'
]

PROJECT_APPS = ['vgl']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'videogames_lair_site.urls'

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

WSGI_APPLICATION = 'videogames_lair_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
use_sqlite_cases = ['test']
use_sqlite = any(use_sqlite_case in sys.argv for use_sqlite_case in use_sqlite_cases) \
             or get_secret('USE_SQLITE', optional=True)

# If we are running tests, use SQLite in memory. Else, use normal DB
if use_sqlite:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'TEST': {
                'NAME': ':memory:'
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'videogames_lair',
            'HOST': 'localhost',
            'PORT': '3306',
            'USER': 'vgl',
            'PASSWORD': get_secret('DB_PASSWORD'),
            'OPTIONS': {
                'charset': 'utf8mb4'
            },
            'TEST': {
                'CHARSET': 'utf8mb4',
                'COLLATION': 'utf8mb4_unicode_ci'
            }
        }
    }

# Cassandra settings
CASSANDRA_HOST = get_secret("CASSANDRA_HOST", is_list=True)
CASSANDRA_USER = get_secret("CASSANDRA_USER")
CASSANDRA_PASSWORD = get_secret("CASSANDRA_PASSWORD")
CASSANDRA_KEYSPACE = "videogames_lair"

# Steam settings
STEAM_KEY = get_secret("STEAM_KEY")

# Test settings
TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"
TEST_OUTPUT_DIR = "reports"
TEST_OUTPUT_FILE_NAME = "report.xml"

# Elasticsearch settings
ES_HOST = get_secret("ES_HOST")

# Authentication settings
AUTH_USER_MODEL = 'vgl.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)

ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_QUERY_EMAIL = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300  # 5 minutes in seconds

ACCOUNT_LOGOUT_REDIRECT_URL = 'vgl:index'
ACCOUNT_LOGOUT_ON_GET = True

LOGIN_URL = "account_login"
# Where to redirect to after login/logout by default
LOGIN_REDIRECT_URL = 'vgl:index'

SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# Send email settings
EMAIL_USE_TLS = True
EMAIL_HOST = get_secret("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = get_secret("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
