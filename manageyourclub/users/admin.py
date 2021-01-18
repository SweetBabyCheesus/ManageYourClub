from django.contrib import admin

from users.models import Gender,CustomUser

# Register your models here.
admin.site.register(Gender)
admin.site.register(CustomUser)
