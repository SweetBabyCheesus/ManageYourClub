from django.test import TestCase, Client
from django.urls import reverse
from clubs.models import ClubModel, AddressModel, PlaceModel
from users.models import CustomUser, Gender
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        
        
        #Ein Testclub muss mithilfe der Modelle erstellt werden um z.B clubViewOrAdd zu testen
        self.place1 = PlaceModel.objects.create(
            postcode = 12345,
            village = "München"
        )
        self.address1 = AddressModel.objects.create(
            streetAddress = 'Teststraße',
            houseNumber = '95b',
            postcode = self.place1
        )
        self.club1 = ClubModel.objects.create(
            clubname = 'fcbayern',
            yearOfFoundation = '1900',
            address = self.address1
        )

        user = CustomUser.objects.create(
            email='testuser@email.de',
            Vorname='Vorname',
            Nachname='Nachname',
            Geburtstag='1997-01-01',
            Geschlecht=Gender.objects.create(gender = 'männlich'),
            Adresse=self.address1) 
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(email='testuser@email.de', password='12345')

        self.addClubView_url = reverse('addclub')
        self.clubViewOrAdd_url = reverse('myclub', kwargs={'club':self.club1.pk})
        self.editClubView_url = reverse('editclub', kwargs={'club':self.club1.pk})
        self.deleteClubView_url = reverse('deleteclub', kwargs={'club':self.club1.pk})
        self.allClubs_url = reverse('allclubs')
        self.requestMembershipView_url = reverse('requestMembership')

    def test_addClubView_GET(self):
        response = self.client.get(self.addClubView_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_club.html')

    def test_clubViewOrAdd_GET(self):
        response = self.client.get(self.clubViewOrAdd_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_club.html')

    def test_editClubView_GET(self):
        response = self.client.get(self.editClubView_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_club.html')

    def test_allClubs_GET(self):
        response = self.client.get(self.allClubs_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_clubs.html')
        
   #status 302??
   #def test_deleteClubView_GET(self):
   #    response = self.client.get(self.deleteClubView_url)
   #    self.assertEquals(response.status_code, 200)

   #def test_requestMembershipView_GET(self):
   #    response = self.client.get(self.requestMembershipView_url)
   #    self.assertEquals(response.status_code, 200)
   #    self.assertTemplateUsed(response, 'all_clubs.html')