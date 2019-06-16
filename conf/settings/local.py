import os

from conf.settings.base import Base


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Local(Base):
    DEBUG = True

    # Testing
    INSTALLED_APPS = Base.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package=api',
    ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
