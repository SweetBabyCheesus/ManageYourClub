from django.shortcuts import render, redirect
from users.models import CustomUser
from notifications.models import MembershipRequest
from clubs.models import ClubModel
from members.models import Membership

def requestNotificationView(request, club):
    #Autor: Max
    #https://www.youtube.com/watch?v=vmP1r6xiJog
    user = request.user

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
    if request.method == 'POST': 
        clubNotId = request.POST.get('clubNotId', None)
        clubNotification = MembershipRequest.objects.get(pk=clubNotId)
        club = clubNotification.club
        userId = clubNotification.user.email
        user = CustomUser.objects.get(email=userId)

        Membership.addMember(club=club, user=user)

        clubNotification.setStatusAccepted()
        return redirect(requestNotificationView, club=club.pk)
    return redirect('home')
    


def declineRequestMembership(request):
    if request.method == 'POST': 
        clubNotId = request.POST.get('clubNotId', None)
        clubNotification = MembershipRequest.objects.get(pk=clubNotId)
        club = clubNotification.club
       
        clubNotification.setStatusDeclined()
    
        return redirect(requestNotificationView, club=club.pk)
    return redirect('home')
