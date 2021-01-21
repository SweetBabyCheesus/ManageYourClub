from django.test import TestCase, Client
from django.urls import reverse
from clubs.models import ClubModel, AddressModel, PlaceModel
from users.models import CustomUser, Gender

def logTestClientIn(client, email='testuser@email.de', password='12345'):
    "Erstellt einen Testnutzer und meldet den übergebenen client mit den Daten des Testnutzers an."
    place = PlaceModel.objects.create(
        postcode = 12345,
        village = "München"
    )

    address = AddressModel.objects.create(
        streetAddress = 'Teststraße',
        houseNumber = '95b',
        postcode = place
    )

    user = CustomUser.objects.create(
        email=email,
        Vorname='Vorname',
        Nachname='Nachname',
        Geburtstag='1997-01-01',
        Geschlecht=Gender.objects.create(gender = 'männlich'),
        Adresse=address
    ) 

    user.set_password(password)
    user.save()
    return client.login(email=email, password=password)

def createTestClub(
    clubname = 'fcbayern',
    yearOfFoundation = '1900',
    streetAddress = 'Teststraße',
    houseNumber = '95b',
    postcode = 12345,
    village = "München"
):
    "Gibt einen Test-Verein zurück"
    place = PlaceModel.objects.create(
        postcode = postcode,
        village = village
    )
    address = AddressModel.objects.create(
        streetAddress = streetAddress,
        houseNumber = houseNumber,
        postcode = place
    )
    return ClubModel.objects.create(
        clubname = clubname,
        yearOfFoundation = yearOfFoundation,
        address = address
    )


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        
        #Ein Testclub muss mithilfe der Modelle erstellt werden um z.B clubViewOrAdd zu testen
        self.club1 = createTestClub()

        logTestClientIn(self.client)

        self.addClubView_url = reverse('addclub')
        self.clubViewOrAdd_url = reverse('myclub', kwargs={'club':self.club1.pk})
        self.editClubView_url = reverse('editclub', kwargs={'club':self.club1.pk})
        self.deleteClubView_url = reverse('deleteclub', kwargs={'club':self.club1.pk})
        self.allClubs_url = reverse('allclubs')
        self.requestMembershipView_url = reverse('requestMembership')

    def test_addClubView_GET(self):
        response = self.client.get(self.addClubView_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_club.html')

    def test_clubViewOrAdd_GET(self):
        response = self.client.get(self.clubViewOrAdd_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'new_club.html')

    def test_editClubView_GET(self):
        response = self.client.get(self.editClubView_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_club.html')

    def test_allClubs_GET(self):
        response = self.client.get(self.allClubs_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_clubs.html')
        
    def test_deleteClubView_GET(self):
        response = self.client.get(self.deleteClubView_url)
        self.assertEqual(response.status_code, 302) #statuscode 302 bei redirect

    def test_requestMembershipView_GET(self):
        response = self.client.get(self.requestMembershipView_url)
        self.assertEqual(response.status_code, 302) #statuscode 302 bei redirect
       # self.assertTemplateUsed(response, 'all_clubs')