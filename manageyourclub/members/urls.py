from django.urls import path
from members.views import clubMembersView

urlpatterns = [
    path('<int:club>/', clubMembersView, name='club_members'),
]