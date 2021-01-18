from django.contrib import admin
from members.models import PaymentMethod, MemberFunction, MemberState, Membership

# Register your models here.

admin.site.register(PaymentMethod)
admin.site.register(MemberFunction)
admin.site.register(MemberState)
admin.site.register(Membership)
