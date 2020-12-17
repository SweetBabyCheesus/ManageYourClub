from django.shortcuts import render
from clubs.models import ClubModel
from members.forms import AddClubMemberForm
from members.models import Membership

# Create your views here.

def clubMembersView(request, club):
    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = AddClubMemberForm(request.POST)
        if form.is_valid():
            form.addMember(club)

    form = AddClubMemberForm()
    memberships = Membership.objects.filter(club=club)
        
    context = {
        'form': form,
        'club': club,
        'memberships': memberships,
    }
    return render(request, 'club_members.html', context)
