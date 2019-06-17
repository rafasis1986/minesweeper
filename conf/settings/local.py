import os

import dj_database_url

from .base import * # noqa

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEBUG = True

# Testing
INSTALLED_APPS += ['django_nose',   # noqa
                   'django_extensions']
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    BASE_DIR,
    '-s',
    '--nologcapture',
    '--with-coverage',
    '--with-progressive',
    '--cover-package=api',
]

DB_URL = os.getenv('DATABASE_URL')

if DB_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600)),
        ),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
