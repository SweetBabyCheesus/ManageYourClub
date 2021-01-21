from django.test import TestCase

class TestModels(TestCase):

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

    def setUp(self):
        self.client = Client()
        
        #Ein Testclub muss mithilfe der Modelle erstellt werden um z.B clubViewOrAdd zu testen
        self.club1 = createTestClub()

        logTestClientIn(self.client)
