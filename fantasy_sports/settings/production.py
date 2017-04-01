from os import environ

from .common import *


SECRET_KEY = environ.get('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': environ.get('DB_DEFAULT_NAME'),
        'HOST': environ.get('DB_DEFAULT_HOST'),
        'PORT': environ.get('DB_DEFAULT_PORT'),
        'USER': environ.get('DB_DEFAULT_USER'),
        'PASSWORD': environ.get('DB_DEFAULT_PASSWORD'),
    },
}

INSTALLED_APPS = INSTALLED_APPS + []
