# Author: Tobias
from django.urls import path
from members.views import clubMembersView, editMemberView

urlpatterns = [
    path('<int:club>/members/', clubMembersView, name='club_members'),
    path('<int:club>/edit/<int:memship>', editMemberView, name='edit_member'),
]