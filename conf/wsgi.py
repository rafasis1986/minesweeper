import os

from configurations.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings.base')
os.environ.setdefault('DJANGO_CONFIGURATION', 'local')

application = get_wsgi_application()
