from django.shortcuts import render, redirect
from teams.models import SportModel, TeamModel
from teams.forms import SportForm, TeamForm, AddTeamMemberForm
from clubs.models import ClubModel
from members.models import Membership


# Funktion teilweise übernommen von https://www.askpython.com/django/django-model-forms
# Tutorial genutzt https://www.geeksforgeeks.org/initial-form-data-django-forms/
def addTeamView(request, club, team=None):
    #Author: Max

    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = TeamForm(request.POST)
        if  form.is_valid():
            form.SetInstanceID(team)
            created = team is None
            team = form.save(club)
            return redirect('showTeam', team=team.pk, club=club.pk)

        else: 
            #falls die Eingaben nicht valide
            return render(request, 'addTeam.html')  
  
    else:

    #if Team is None -> Hinzufügen 
    #else: Falls der user einen nicht existierenden Verein bearbeiten möchte
        if team is None:
            instance = None
            initial = {}
        else: 
            if not TeamModel.objects.filter(pk=team).exists():
                return redirect('addTeam')

            instance = TeamModel.objects.get(pk=team)
            initial = {
                'sportName' : instance.sportId.sportName,
                'clubId' : instance.clubId,
                'teamName' : instance.teamName,
            }

        form = TeamForm(instance=instance, initial=initial)
        
        context = {
            'form':form,
            'team':instance,
            'club':club,
        }
        
        if team is not None:
            return render(request, 'editTeam.html', context) 
    return render(request, 'addTeam.html', context)


def showTeamView(request, team, club):
    #Author: Max

    team = TeamModel.objects.get(pk=team)
    club = ClubModel.objects.get(pk=club)

    if not TeamModel.objects.filter(pk=team.pk).exists():
            return redirect('addTeam')
    
    context = {
    'team':team,
    'club':club,
    }   

    return render(request, 'showTeam.html', context)

def showAllTeams(request, club):
    #Author: Max

    club = ClubModel.objects.get(pk=club)

    teams = TeamModel.objects.filter(clubId=club)

    context = {
        'teams': teams,
        'club': club,
    }

    return render(request, 'showAllTeams.html', context)


def deleteTeamView(request, team, club):
    #Author: Max

    team = TeamModel.objects.get(pk=team)

    if request.method == 'POST':
        sport = team.sportId    
        team.delete()
        if not TeamModel.objects.filter(sportId=sport).exists():
            sport.delete()

        return redirect('/?Mannschaft_wurde_gelöscht:_'+str(team))

    return redirect('/?Mannschaft_'+ +str(team)+'_wurde_NICHT_gelöscht.')



def editTeamMembersView(request, team, club):
    #Autor: Max
    club = ClubModel.objects.get(pk=club)
    team = TeamModel.objects.get(pk=team)

    teamMembers = team.members.all()  
    form = AddTeamMemberForm()

    if request.method == 'POST': # Wird nach klicken auf Mitglied hinzufügen

        form = AddTeamMemberForm(request.POST)

        if form.is_valid():
            form.addMember(club, team)

    context = {
        'form': form,
        'team': team,
        'club': club,
        'teamMembers': teamMembers,
    }



    return render(request, 'teamMemberHandling\editTeamMembers.html', context)


