from django.contrib import admin
from clubs.models import PlaceModel, AddressModel, ClubModel

# Register your models here.

admin.site.register(PlaceModel)
admin.site.register(AddressModel)
admin.site.register(ClubModel)
