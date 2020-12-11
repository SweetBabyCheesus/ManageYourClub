from django.urls import path
from clubs.views import AddClubView, ClubViewOrAdd, DeleteClubView

# Tutorial genutzt: https://dev-yakuza.posstree.com/en/django/form/

urlpatterns = [
    path('addclub/', AddClubView, name='addclub'),
    path('<int:pk>/', ClubViewOrAdd, name='myclub'),
    path('edit/<int:pk>/', AddClubView, name='editclub'),
    path('delete/<int:pk>/', DeleteClubView, name='deleteclub'),
]