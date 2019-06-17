import os

from .base import * # noqa

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = ['*']
INSTALLED_APPS += ['gunicorn']  # noqa
