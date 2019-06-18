import os

import dj_database_url

from .base import * # noqa


SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 60)),
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        },
    },
}

EMAIL_SUBJECT_PREFIX = os.getenv(
    'DJANGO_EMAIL_SUBJECT_PREFIX', '[Minesweeper-API]',
)

INSTALLED_APPS += ['gunicorn']  # noqa
