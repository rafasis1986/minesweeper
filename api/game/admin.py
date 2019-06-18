from api.game import models

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.Game)


@admin.register(models.Player)
class UserAdmin(UserAdmin):
    pass
