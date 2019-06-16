from django.conf.urls import include, url
from django.contrib import admin


API_VERSION = 1

urlpatterns = [
    url('{0}/'.format(API_VERSION), include([
        url(r'^admin/', admin.site.urls),
    ])),
]
