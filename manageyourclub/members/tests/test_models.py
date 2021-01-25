# Author: Tobias
from django.test import TestCase
from members.models import Membership, club_has_member
from clubs.tests.test_views import createTestClub, createTestUser

class TestModels(TestCase):
    
    def setUp(self):
        "Vorbereitung für die Tests"
        self.club = createTestClub(clubname='Die Tester')
        self.user = createTestUser()

    def test_addMember(self):
        """
            Testinhalt:
            Der Angegebene Nutzer sollte zum Mitglied beim angegebenen Verein werden.
        """
        self.assertFalse(club_has_member(self.club, self.user))
        Membership.addMember(self.club, self.user)
        self.assertTrue(club_has_member(self.club, self.user))
