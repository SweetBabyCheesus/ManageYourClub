from django.test import TestCase, Client
from django.urls import reverse
from members.views import clubMembersView, editMemberView
from clubs.models import ClubModel, AddressModel
from users.models import CustomUser, Gender
from clubs.tests.test_views import createTestUser, createTestClub, logTestClientIn

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.club1 = createTestClub()

        logTestClientIn(self.client)

        self.clubMembersView_url = reverse('club_members', kwargs={'club':self.club1.pk})
        self.editMemberView_url = reverse('club_members', kwargs={'club':self.club1.pk})

    def test_clubMembersView_GET(self):
        response = self.client.get(self.clubMembersView_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_members.html')

    def test_editMemberView_GET(self):
        response = self.client.get(self.editMemberView_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_members.html')