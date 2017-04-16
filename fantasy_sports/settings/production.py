from os import environ

from .common import *


DEBUG = False

SECRET_KEY = environ.get('SECRET_KEY')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_SUBJECT_PREFIX = '[Fantasy Sports] '

ALLOWED_HOSTS = ['rbennett.io']

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
