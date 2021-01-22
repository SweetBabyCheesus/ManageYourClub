# Author: Tobias
from django.test import TestCase, Client
from django.urls import reverse
from clubs.tests.test_views import logTestClientIn, createTestClub
from teams.models import SportModel, TeamModel
from members.models import Membership

def createTestTeam(club, members=None, teamName='Tester', sportname='Testing'):
    "Erstellt eine Mannschaft für den angegebenen Verein"
    sport = SportModel.objects.get_or_create(sportName=sportname)[0]

    team = TeamModel.objects.create(clubId=club, teamName=teamName, sportId=sport)
    if members:
        team.members.set(members)
    team.save()
    return team

class TestViews(TestCase):

    def setUp(self):
        "Vorbereitung für die Tests"
        self.client = Client()
        
        self.club = createTestClub()

        self.team = createTestTeam(self.club)

        logTestClientIn(self.client)

        Membership.addMember(self.club, self.client.user)

        self.addTeamView_add_url = reverse('addTeam', kwargs={'club':self.club.pk})
        self.addTeamView_edit_url = reverse('editTeam', kwargs={'club':self.club.pk, 'team':self.team.pk})
        self.showTeam_url = reverse('showTeam', kwargs={'club':self.club.pk, 'team':self.team.pk})
        self.showAllTeams_url = reverse('showAllTeams', kwargs={'club':self.club.pk})
        self.deleteTeam_url = reverse('deleteTeam', kwargs={'team':self.team.pk})
        self.addTeamMember_url = reverse('addTeamMember', kwargs={'club':self.club.pk, 'team':self.team.pk})

    def test_addTeamView_add_GET(self):
        """
            Testinhalt: 
            Wenn keine Mannschaft angegeben ist, sollte die Erstellungsansicht für Mannschaften angezeigt werden.
        """
        response = self.client.get(self.addTeamView_add_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'addTeam.html')

    def test_addTeamView_edit_GET(self):
        """
            Testinhalt: 
            Wenn eine Mannschaft angegeben wurde sollte die Bearbeitungsansicht der Mannschaft angezeigt werden.
        """
        response = self.client.get(self.addTeamView_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editTeam.html')
        self.assertTrue(response.context.__contains__('team'))
        self.assertEqual(response.context['team'], self.team)

    def test_addTeamView_add_POST(self):
        """
            Testinhalt: 
            Wenn in der URL keine Mannschaft angegeben wurde und ein valides Formular
            per POST versandt wird, sollte eine Mannschaft erstellt werden.
            Außerdem sollte der Nutzer weitergeleitet werden. 
        """
        teamName = 'Testgruppe 1'
        response = self.client.post(self.addTeamView_add_url, {
            'teamName': teamName,
            'sportName': self.team.sportId.sportName
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamModel.objects.all().filter(teamName=teamName).exists())

    def test_addTeamView_edit_POST(self):
        """
            Testinhalt: 
            Wenn in der URL eine Mannschaft angegeben wurde und per POST ein valides
            Formular übergeben wurde, sollten die Daten der Mannschaft entsprechend 
            geändert werden.
        """
        teamName = 'Testgruppe 2'
        response = self.client.post(self.addTeamView_edit_url, {
            'teamName': teamName,
            'sportName': self.team.sportId.sportName
        })
        self.assertEqual(response.status_code, 302)
        self.team = TeamModel.objects.get(pk=self.team.pk) # aktualisiert die Mannschaftsdaten
        self.assertEqual(self.team.teamName, teamName)

    def test_showTeamView_GET(self):
        """
            Testinhalt: 
            Die Detailansicht der in der URL angegebenen Mannschaft sollte angezeigt werden.
        """
        response = self.client.get(self.showTeam_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'showTeam.html')
        self.assertTrue(response.context.__contains__('team'))
        self.assertEqual(response.context['team'], self.team)

    def test_showAllTeams_GET(self):
        """
            Testinhalt: 
            Die Übersicht aller Mannschaften sollte angezeigt werden.
        """
        response = self.client.get(self.showAllTeams_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'showAllTeams.html')
        self.assertTrue(response.context.__contains__('teams'))
        self.assertTrue(response.context['teams'].filter(teamName=self.team.teamName).exists())

    def test_deleteTeamView_GET(self): 
        """
            Testinhalt:
            Man sollte weitergeleitet werden, ohne dass die Mannschaft gelöscht wird.
        """
        response = self.client.get(self.deleteTeam_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TeamModel.objects.all().filter(pk=self.team.pk).exists())

    def test_deleteTeamView_POST(self): 
        """
            Testinhalt:
            Man sollte weitergeleitet werden, nachdem die Mannschaft gelöscht wurde.
        """
        response = self.client.post(self.deleteTeam_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(TeamModel.objects.all().filter(pk=self.team.pk).exists())

    def test_addTeamMemberView_GET(self): 
        """
            Testinhalt:
            Die Übersicht aller Mitglieder sollte angezeigt werden.
        """
        response = self.client.get(self.addTeamMember_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teamMemberHandling/addTeamMember.html')
        
    def test_addTeamMemberView_POST(self): 
        """
            Testinhalt:
            Die Übersicht aller Mitglieder sollte angezeigt werden.
            Das übergebene Mitlgied sollte zur Mannschaft hinzugefügt werden.
        """
        response = self.client.post(self.addTeamMember_url, {'eMail':self.client.user})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teamMemberHandling/addTeamMember.html')
        self.team = TeamModel.objects.get(pk=self.team.pk) # aktualisiert die Mannschaftsdaten
        self.assertTrue(self.team.members.filter(pk=self.client.user.pk).exists())
        self.assertTrue(self.team)
        
    
    # FIXME fehlt noch: addTeamMember_POST  
        