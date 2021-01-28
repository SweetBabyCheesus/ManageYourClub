# Author: Tobias
from django.test import TestCase, Client
from clubs.tests.test_views import logTestClientIn, createTestClub
from teams.tests.test_views import createTestTeam
from members.models import Membership
from teams.forms import TeamForm, AddTeamMemberForm
from teams.models import TeamModel

class TestForms(TestCase):

    def setUp(self):
        "Vorbereitung für die Tests"
        self.client = Client()
        self.club = createTestClub()
        self.team = createTestTeam(self.club)
        logTestClientIn(self.client)
        Membership.addMember(self.club, self.client.user)

    def test_TeamForm_is_valid(self):
        """
            Testinhalt: 
            Sollte True zurückgeben, wenn zwei Strings der Länge 1 bis 30 im Formular eingetragen wurden.
            Ansonsten sollte False zurückgegeben werden.
        """
        form = TeamForm({'teamName':'Die Tester', 'sportName':'Testen'})
        self.assertTrue(form.is_valid())
        
        form = TeamForm({})
        self.assertFalse(form.is_valid())

    def test_TeamForm_setInstanceID(self):
        """
            Testinhalt: 
            Sollte den übergebenen Wert in die Variable pk schreiben
        """
        form = TeamForm()
        form.SetInstanceID(None)
        self.assertIsNone(form.pk)
        form.SetInstanceID(42)
        self.assertEqual(form.pk, 42)

    def test_TeamForm_save(self):
        """
            Testinhalt: 
            Wenn pk auf None gesetzt wurde sollte eine Mannschaft mit den im Formular übergebenen Daten 
            erstellt werden.
            Ansonsten sollte eine bereits bestehende Mannschaft mit dem in pk gespeicherten Primary Key 
            entsprechend bearbeitet werden. 
        """
        teamName = 'Die Tester'
        sportName = 'Testen'
        form = TeamForm({'teamName':teamName, 'sportName':sportName})
        self.assertTrue(form.is_valid())
        form.SetInstanceID(None)
        team = form.save(self.club)
        self.assertIsNotNone(team)
        self.assertEqual(team.sportId.sportName, sportName)
        self.assertEqual(team.teamName, teamName)
        self.assertTrue(TeamModel.objects.filter(pk=team.pk).exists())


        teamName2 = teamName+'2'
        sportName2 = sportName+'2'
        form = TeamForm({'teamName':teamName2, 'sportName':sportName2})
        self.assertTrue(form.is_valid())
        form.SetInstanceID(team.pk)
        team2 = form.save(self.club)
        self.assertIsNotNone(team2)
        self.assertEqual(team2.sportId.sportName, sportName2)
        self.assertEqual(team2.teamName, teamName2)

        self.assertEqual(team2.pk, team.pk)

    def test_AddTeamMemberForm_is_valid(self):
        """
            Testinhalt: 
            Sollte True zurückgeben, wenn ein String der Länge 1 bis 50 im Formular eingetragen wurde.
            Ansonsten sollte False zurückgegeben werden.
        """
        form = AddTeamMemberForm({'eMail':self.client.user.email})
        self.assertTrue(form.is_valid())

        form = AddTeamMemberForm({})
        self.assertFalse(form.is_valid())

    def test_AddTeamMemberForm_addMember(self): # FIXME
        """
            Testinhalt: 
            Sollte den Nutzer mit der im Formular übergebenen E-Mail-Adresse als Mitglied zur Mannschaft 
            hinzufügen, wenn er ein Mitglied bei dem entsprechenden Verein ist.
            Wenn der Nutzer kein Mitglied im Verein ist, sollte er nicht zur Mannschaft hinzugefügt werden.
            Wenn der Nutzer bererits Mitglied der Mannschaft ist, sollte er nicht nocheinmal hinzugefügt werden.
        """
        form = AddTeamMemberForm({'eMail':self.client.user.email})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(self.team.members.all()), 0)
        self.assertFalse(self.team.members.filter(member=self.client.user).exists())
        form.addMember(self.club, self.team)
        self.assertEqual(len(self.team.members.all()), 1)
        self.assertTrue(self.team.members.filter(member=self.client.user).exists())
        form.addMember(self.club, self.team)
        self.assertEqual(len(self.team.members.all()), 1)


