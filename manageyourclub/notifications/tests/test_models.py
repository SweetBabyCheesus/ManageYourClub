# Author: Tobias
from django.test import TestCase
from notifications.models import MembershipRequest
from members.models import Membership
from clubs.tests.test_views import createTestClub, createTestUser

class TestModels(TestCase):
    
    def setUp(self):
        "Vorbereitung für die Tests"
        self.club = createTestClub(clubname='Die Tester')
        self.user1 = createTestUser(email='test1@email.de')
        self.user2 = createTestUser(email='test2@email.de')
        self.memshipRequest = MembershipRequest.addRequest(self.user1, self.club, 1)

    def test__str__(self):
        """
            Testinhalt:
            Der Rückgabewert sollte zum Muster 'user: <email-Adresse>, club: <Vereinsname>' passen.
        """
        self.assertEqual("user: test1@email.de, club: Die Tester", self.memshipRequest.__str__())

    def test_addRequest(self):
        """
            Testinhalt:
            Wenn der die Beitrittsanfrage oder die dazu passende Mitgliedschaft noch nicht existiert,
            sollte die Beitrittsanfrage passend zur Eingabe und mit Status 1 erstellt und zurückgegeben werden. 
            Ansonsten sollte None zurückgegeben werden.
        """
        direction = 1
        request = MembershipRequest.addRequest(self.user2, self.club, direction)
        self.assertEqual(request.user, self.user2)
        self.assertEqual(request.club, self.club)
        self.assertEqual(request.direction, direction)
        self.assertEqual(request.status, 1)

        # da request schon existiert sollte beim erneuten Aufruf mit den selben Parametern None zurückgegeben werden:
        self.assertIsNone(MembershipRequest.addRequest(self.user2, self.club, direction))

        request.delete()
        Membership.addMember(self.club, self.user2)
        # da die entsprechende Mitgliedschaft schon existiert sollte None zurückgegeben werden:
        self.assertIsNone(MembershipRequest.addRequest(self.user2, self.club, direction))

    def test_setStatusAccepted(self):
        """
            Testinhalt:
            Der Status der Beitrittsanfrage sollte sich zu 2 ändern
        """
        self.memshipRequest.setStatusAccepted()
        self.assertEqual(self.memshipRequest.status, 2)

    def test_setStatusDeclined(self):
        """
            Testinhalt:
            Der Status der Beitrittsanfrage sollte sich zu 3 ändern
        """
        self.memshipRequest.setStatusDeclined()
        self.assertEqual(self.memshipRequest.status, 3)