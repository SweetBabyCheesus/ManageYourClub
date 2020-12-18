from django.urls import path
from members.views import clubMembersView, editMemberView

urlpatterns = [
    path('<int:club>/', clubMembersView, name='club_members'),
    path('edit/<int:memship>', editMemberView, name='edit_member')
]