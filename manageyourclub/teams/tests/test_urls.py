# Author: Tobias
# Tutorial genutzt: https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from teams.views import addTeamView, showTeamView, showAllTeams, deleteTeamView, addTeamMemberView

class TestUrls(SimpleTestCase):

    def test_addTeam_url_is_resolved(self):
        url = reverse('addTeam', args=[1])
        self.assertEqual(resolve(url).func, addTeamView)

    def test_showTeam_url_is_resolved(self):
        url = reverse('showTeam', args=[1, 1])
        self.assertEqual(resolve(url).func, showTeamView)

    def test_addTeamMember_url_is_resolved(self):
        url = reverse('addTeamMember', args=[1, 1])
        self.assertEqual(resolve(url).func, addTeamMemberView)

    def test_editTeam_url_is_resolved(self):
        url = reverse('editTeam', args=[1, 1])
        self.assertEqual(resolve(url).func, addTeamView)      

    def test_showAllTeams_url_is_resolved(self):
        url = reverse('showAllTeams', args=[1])
        self.assertEqual(resolve(url).func, showAllTeams)

    def test_deleteTeam_url_is_resolved(self):
        url = reverse('deleteTeam', args=[1])
        self.assertEqual(resolve(url).func, deleteTeamView)   