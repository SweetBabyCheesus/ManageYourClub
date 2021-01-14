from django.urls import path
from clubs.views import addClubView, clubViewOrAdd, deleteClubView, allClubs, requestMembershipView

# Tutorial genutzt: https://dev-yakuza.posstree.com/en/django/form/

urlpatterns = [
    path('addclub/', addClubView, name='addclub'),
    path('<int:club>/', clubViewOrAdd, name='myclub'),
    path('edit/<int:club>/', addClubView, name='editclub'),
    path('delete/<int:club>/', deleteClubView, name='deleteclub'),
    path('allclubs/', allClubs, name='allclubs'),
    path('requestMembership/', requestMembershipView, name='requestMembership'),
]