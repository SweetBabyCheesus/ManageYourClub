# Author: Tobias
from django.shortcuts import render, redirect
from clubs.models import ClubModel
from members.forms import AddClubMemberForm, editMemberForm
from members.models import Membership
from users.models import CustomUser
from django.contrib import messages


# Create your views here.

# Tutorial genutzt https://www.youtube.com/watch?v=F5mRW0jo-U4&t=1358s (ab 2:14:16)
def clubMembersView(request, club):
    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': # Wird nach klicken auf Mitglied Löschen ausgeführt
        print("POST wird ausgeführt.")
        form = AddClubMemberForm(request.POST)
        if form.is_valid():
            eMail = form.cleaned_data['eMail']
            if(CustomUser.objects.filter(email=eMail).exists()):
                member=CustomUser.objects.get(email=eMail)
                if(Membership.objects.filter(club=club, member=member).exists()):
                    messages.error(request, 'Der Benutzer mit der E-Mail-Adresse "'+member.email+'" ist bereits Mitglied des Vereins.')
                else:
                    form.addMember(club=club)
                    messages.success(request, 'Der Benutzer mit der E-Mail-Adresse "'+member.email+'" wurde zum Verein hinzugefügt.')
            else:
                messages.error(request, 'Es existiert kein Benutzer mit der E-Mail-Adresse "'+eMail+'".')
        else:
            membership = request.POST.get('membership')
            if(Membership.objects.filter(pk=membership).exists()):
                membership = Membership.objects.get(pk=membership)
                print('DELETE ' + str(membership.delete()))
        return redirect('club_members', club.pk)

    form = AddClubMemberForm()
    #deleteMemberForm = DeleteClubMemberForm()
    memberships = Membership.objects.filter(club=club)
        
    context = {
        'form': form,
        #'delMemForm': deleteMemberForm,
        'club': club,
        'memberships': memberships,
    }
    return render(request, 'club_members.html', context)

# Tutorial genutzt: https://www.geeksforgeeks.org/initial-form-data-django-forms/
def editMemberView(request, club, memship):
    club = ClubModel.objects.get(pk=club)
    memship = Membership.objects.get(pk=memship)
    
    initial = {
        'memberFunction':memship.memberFunction,
    }

    form = editMemberForm(initial=initial)

    context = {
        'form': form,
        'club': club,
        'membership': memship,
    }

    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = editMemberForm(request.POST)
        if form.is_valid():
            form.saveChanges(memship)
        return redirect('club_members', club.pk)

    return render(request, 'edit_member.html', context)