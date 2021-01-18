from django.contrib import admin

from teams.models import SportModel,TeamModel

# Register your models here.
admin.site.register(SportModel)
admin.site.register(TeamModel)