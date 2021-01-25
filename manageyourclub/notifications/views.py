from django.shortcuts import render, redirect
from users.models import CustomUser
from notifications.models import MembershipRequest
from clubs.models import ClubModel
from members.models import Membership

def requestNotificationView(request, club):
    #Autor: Max
    #https://www.youtube.com/watch?v=vmP1r6xiJog
    user = request.user

    #Zur anzeige der Vereinsbezogenen Anfragen: Filterung
    if ClubModel.objects.filter(pk=club).exists():
        club = ClubModel.objects.get(pk=club)
    clubNotifications = MembershipRequest.objects.filter(club=club)

    context = {
        'user':user,
        'club':club,
        'clubNotifications':clubNotifications,
    }
    
    return render(request, 'showNotifications.html', context)

def acceptRequestMembership(request):
    #Autor: Max
    #Funktion um Mitgliedsanfragen von Usern an Vereine anzunehmen

    if request.method == 'POST': 
        clubNotId = request.POST.get('clubNotId', None)
        clubNotification = MembershipRequest.objects.get(pk=clubNotId)
        club = clubNotification.club
        userId = clubNotification.user.email
        user = CustomUser.objects.get(email=userId)

        #Erstellung der Mitgliedschaft mit den übergebenen Daten
        Membership.addMember(club=club, user=user)

        #Anpassung des Mitteilungsstatus auf angenommen
        clubNotification.setStatusAccepted()
        return redirect(requestNotificationView, club=club.pk)
    return redirect('home')
    


def declineRequestMembership(request):
    #Autor: Max
    #Funktion um Mitgliedsanfragen von Usern an Vereine abzulehnen

    if request.method == 'POST': 
        clubNotId = request.POST.get('clubNotId', None)
        clubNotification = MembershipRequest.objects.get(pk=clubNotId)
        club = clubNotification.club
       
        #Anpassung des Mitteilungsstatus auf abgelehnt
        clubNotification.setStatusDeclined()
    
        return redirect(requestNotificationView, club=club.pk)
    return redirect('home')
