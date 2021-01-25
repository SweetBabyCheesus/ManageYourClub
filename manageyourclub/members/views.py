# Author: Tobias
from django.shortcuts import render, redirect
from clubs.models import ClubModel
from members.forms import AddClubMemberForm, editMemberForm
from members.models import Membership

# Create your views here.

# Tutorial genutzt https://www.youtube.com/watch?v=F5mRW0jo-U4&t=1358s (ab 2:14:16)
def clubMembersView(request, club):
    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': # Wird nach klicken auf Mitglied Löschen ausgeführt
        form = AddClubMemberForm(request.POST)
        if form.is_valid():
            form.addMember(club)
        else:
            membership = request.POST.get('membership')
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