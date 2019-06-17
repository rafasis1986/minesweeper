from api.game.views import GameViewSet

from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers


API_VERSION = 1

router = routers.DefaultRouter()

router.register(r'games', GameViewSet, base_name='api_games')

urlpatterns = [
    url('v{0}/'.format(API_VERSION), include([
        url(r'^admin/', admin.site.urls),
        url(r'^api/', include(router.urls)),
    ])),
]
