from django.urls import path
from clubs.views import AddClubView, ClubView



urlpatterns = [
    path('addclub/', AddClubView, name='addclub'),
    path('myclub/', ClubView.as_view(), name='myclub'),
]