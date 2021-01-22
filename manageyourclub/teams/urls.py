from django.urls import path
from teams.views import addTeamView, showTeamView, showAllTeams, deleteTeamView, addTeamMemberView

# Tutorial genutzt: https://dev-yakuza.posstree.com/en/django/form/

urlpatterns = [
    #wichtig: übergabe der Club/ Team Variable mit Get Methode
    path('<int:club>/addTeam/', addTeamView, name='addTeam'),
    path('<int:club>/<int:team>/showTeam', showTeamView, name='showTeam'),
    path('<int:club>/<int:team>/addTeamMember/', addTeamMemberView, name='addTeamMember'),
    path('<int:club>/<int:team>/editTeam/', addTeamView, name='editTeam'),
    path('<int:club>/showAllTeams/', showAllTeams, name='showAllTeams'),
    path('<int:team>/delete/', deleteTeamView, name='deleteTeam'),
]
