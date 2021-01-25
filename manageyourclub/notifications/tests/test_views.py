# Author: Tobias
from django.test import TestCase, Client
from django.urls import reverse
from clubs.tests.test_views import logTestClientIn, createTestClub
from notifications.models import MembershipRequest

class TestViews(TestCase):

    def setUp(self):
        "Vorbereitung für die Tests"
        self.client = Client()
        
        self.club = createTestClub()

        logTestClientIn(self.client)

        self.memshipRequest = MembershipRequest.addRequest(self.client.user, self.club, 1)

        self.requestNotifications_url = reverse('requestNotifications', kwargs={'club':self.club.pk})
        self.acceptRequestMembership_url = reverse('acceptRequestMembership')
        self.declineRequestMembership_url = reverse('declineRequestMembership')

    def test_requestNotificationView_GET(self):
        """
            Testinhalt: 
            Es sollte die Nachrichtenübersicht des in der URL übergebenen Vereins angezeigt werden.
        """
        response = self.client.get(self.requestNotifications_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'showNotifications.html')

    def test_acceptRequestMembership_GET(self):
        """
            Testinhalt: 
            Bei GET soll man weitergeleitet werden.
        """
        response = self.client.get(self.acceptRequestMembership_url, {'clubNotId': self.memshipRequest.pk})
        self.assertEqual(response.status_code, 302)

    def test_acceptRequestMembership_POST(self):
        """
            Testinhalt: 
            Die versandte Beitrittsanfrage sollte angenommen werden.
            Außerdem sollte der Benutzer weitergeleitet werden.
        """
        self.assertEqual(self.memshipRequest.status, 1)
        response = self.client.post(self.acceptRequestMembership_url, {'clubNotId': self.memshipRequest.pk})
        memshipRequest = MembershipRequest.objects.get(user=self.client.user, club=self.club, direction=1)
        self.assertEqual(memshipRequest.status, 2)
        self.assertEqual(response.status_code, 302)

    def test_declineRequestMembership_GET(self):
        """
            Testinhalt: 
            Bei GET soll man weitergeleitet werden.
        """
        response = self.client.get(self.declineRequestMembership_url, {'clubNotId': self.memshipRequest.pk})
        self.assertEqual(response.status_code, 302)
        
    def test_declineRequestMembership_POST(self):
        """
            Testinhalt: 
            Die versandte Beitrittsanfrage sollte abgelehnt werden.
            Außerdem sollte der Benutzer weitergeleitet werden.
        """
        self.assertEqual(self.memshipRequest.status, 1)
        response = self.client.post(self.declineRequestMembership_url, {'clubNotId': self.memshipRequest.pk})
        memshipRequest = MembershipRequest.objects.get(user=self.client.user, club=self.club, direction=1)
        self.assertEqual(memshipRequest.status, 3)
        self.assertEqual(response.status_code, 302)
        