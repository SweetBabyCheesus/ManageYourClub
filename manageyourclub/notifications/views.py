from django.shortcuts import render, redirect
from members.models import MemberState
from users.models import CustomUser
from clubs.models import ClubModel
from members.models import Membership

"""
def requestNotificationView(request, club):
    #Autor: Max
    #https://www.youtube.com/watch?v=vmP1r6xiJog
    #Im Sprint 9 wurde das Design ueberarbeitet. Die Funktionalität wird daher aktuell in users.views abgebildet.
    #Nach der Abgabe wollen wir unsere Startseite ggf nochmal überarbeiten. Um die Benachitigungen dan neu einzubinden, bleibt diese Methode vorerst erhalten.

    user = request.user

    #Zur anzeige der Vereinsbezogenen Anfragen: Filterung
    if ClubModel.objects.filter(pk=club).exists():
        club = ClubModel.objects.get(pk=club)
    membershipRequestNotifications = Membership.objects.filter(club=club,MemberState=0)

    context = {
        'user':user,
        'club':club,
        'membershipRequestNotifications':membershipRequestNotifications,
    }
    
    return render(request, 'showNotifications.html', context)



def acceptRequestMembership(request):
    #Autor: Max
    #Funktion um Mitgliedsanfragen von Usern an Vereine anzunehmen
    #TODO: Anpassen für Thesis

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
    #TODO: Anpassen für Thesis

    if request.method == 'POST': 
        clubNotId = request.POST.get('clubNotId', None)
        clubNotification = MembershipRequest.objects.get(pk=clubNotId)
        club = clubNotification.club
       
        #Anpassung des Mitteilungsstatus auf abgelehnt
        clubNotification.setStatusDeclined()
    
        return redirect(requestNotificationView, club=club.pk)
    return redirect('home')
"""