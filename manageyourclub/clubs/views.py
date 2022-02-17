# Author: Tobias

from django.shortcuts import render, redirect
from clubs.forms import AddClubForm
from clubs.models import ClubModel, AddressModel
from members.models import club_has_member, Membership
from notifications.models import MembershipRequest

def allClubs(request):
    user = request.user

    #myClubs Liste von Max hinzugefügt um Beziehung zu den Vereinen im Template darzustellen
    Memberships = Membership.objects.filter(member=user)
    myClubs = []
    for membership in Memberships:
        myClubs.append(membership.club)


    context = {
        'Memberships':Memberships,
        'clubs': ClubModel.objects.all(),
        'myClubs':myClubs,
    }

    if not ClubModel.objects.all().exists():
        return redirect('addclub')

    return render(request, 'all_clubs.html', context)

# Tutorial genutzt: https://www.youtube.com/watch?v=F5mRW0jo-U4&t=1358s (2:58:24)
def clubViewOrAdd(request, club):
    if not ClubModel.objects.filter(pk=club).exists():
        return redirect('addclub')
    
    club = ClubModel.objects.get(pk=club)
    club_list = filter(
                lambda c: 
                    club_has_member(c, request.user), 
                ClubModel.objects.all()
            )
    
    context = {
        'club'     : club,
        'club_list': club_list,
        'to'         : 'myclub',
    }
    return render(request, 'my_club.html', context)


def editClubView(request, club):
    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = AddClubForm(request.POST)
        if form.is_valid():
            form.edit(club)
            return redirect('myclub', club)
    else:
        if not ClubModel.objects.filter(pk=club).exists():
            return redirect('addclub')
        instance = ClubModel.objects.get(pk=club)
        initial = {
            'streetAddress' : instance.address.streetAddress,
            'houseNumber'   : instance.address.houseNumber,
            'postcode'      : instance.address.postcode.postcode,
            'village'       : instance.address.postcode.village
        }
        form = AddClubForm(instance=instance, initial=initial)
        
        context = {
            'form':form,
            'club':instance,
        }
        
        return render(request, 'edit_club.html', context)

# Funktion teilweise übernommen von https://www.askpython.com/django/django-model-forms
# Tutorial genutzt https://www.geeksforgeeks.org/initial-form-data-django-forms/
def addClubView(request):
    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = AddClubForm(request.POST)
        if form.is_valid():
            club = form.create()
            Membership.addMember(club=club, user=request.user)
            return redirect('myclub', club.pk)
    else:        
        form = AddClubForm()
        
        context = {
            'form':form,
        }
        
    return render(request, 'new_club.html', context)

def deleteClubView(request, club):
    club = ClubModel.objects.get(pk=club)
    if request.method == 'POST':
        adr = club.address    
        club.delete()
        if not ClubModel.objects.filter(address=adr).exists():
            pc = adr.postcode
            adr.delete()
            if not AddressModel.objects.filter(postcode=pc).exists():
                pc.delete()
        return redirect('/?Verein_wurde_gelöscht:_'+str(club))
    return redirect('/?Verein_wurde_NICHT_gelöscht:_'+str(club))

    





def requestMembershipView(request):
    #Autor Max
    #Funktion um als User die Mitgliedschaft in einem Verein anzufrageen
    context={}

    if request.method == 'POST': 
        clubId = request.POST.get('clubId', None)
        club = ClubModel.objects.get(pk=clubId)
        user = request.user
        direction = 1

        #Erstellung eines MembershipRequest objectes, damit der Verein annehmen oder ablehnen kann
        MembershipRequest.addRequest(user=user, club=club, direction=direction)

    return redirect('allclubs')