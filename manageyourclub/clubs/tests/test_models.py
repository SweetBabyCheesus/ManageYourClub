from django.test import TestCase, Client
from django.urls import reverse
from clubs.models import ClubModel, AddressModel
from users.models import CustomUser, Gender
from clubs.tests.test_views import createTestUser, createTestClub, logTestClientIn

class TestModels(TestCase):

    def setUp(self):
        self.client = Client()
        
        #Ein Testclub muss mithilfe der Modelle erstellt werden um z.B clubViewOrAdd zu testen
        self.club = createTestClub()
        self.user = createTestUser()
    
    def test_AddressModel_create(self):
        address = AddressModel.create(
            self.user.Adresse.streetAddress,
            self.user.Adresse.houseNumber,
            self.user.Adresse.postcode.postcode,
            self.user.Adresse.postcode.village
        )

        self.assertEqual(self.user.Adresse.streetAddress, address.streetAddress)
        self.assertEqual(self.user.Adresse.houseNumber, address.houseNumber)
        self.assertEqual(self.user.Adresse.postcode.postcode, address.postcode.postcode)
        self.assertEqual(self.user.Adresse.postcode.village, address.postcode.village)

    def test_AddressModel_get_or_create(self):
        address = AddressModel.get_or_create(
            self.user.Adresse.streetAddress,
            self.user.Adresse.houseNumber,
            self.user.Adresse.postcode.postcode,
            self.user.Adresse.postcode.village
        )

        self.assertEqual(self.user.Adresse.streetAddress, address.streetAddress)
        self.assertEqual(self.user.Adresse.houseNumber, address.houseNumber)
        self.assertEqual(self.user.Adresse.postcode.postcode, address.postcode.postcode)
        self.assertEqual(self.user.Adresse.postcode.village, address.postcode.village)

    def test_ClubModel_create(self):
        club1 = ClubModel.create(
            self.club.clubname,
            self.club.yearOfFoundation,
            self.user.Adresse.streetAddress,
            self.user.Adresse.houseNumber,
            self.user.Adresse.postcode.postcode,
            self.user.Adresse.postcode.village
        )

        self.assertEqual(self.club.clubname, club1.clubname)
        self.assertEqual(self.club.yearOfFoundation, club1.yearOfFoundation)

    def test_ClubModel_get_orcreate(self):
        club1 = ClubModel.get_or_create(
            self.club.clubname,
            self.club.yearOfFoundation,
            self.user.Adresse.streetAddress,
            self.user.Adresse.houseNumber,
            self.user.Adresse.postcode.postcode,
            self.user.Adresse.postcode.village
        )

        self.assertEqual(self.club.clubname, club1.clubname)
        self.assertEqual(self.club.yearOfFoundation, club1.yearOfFoundation)
        
    def test_ClubModel_edit(self):
        club1 = ClubModel.edit(
            self.club,
            self.club.clubname,
            self.club.yearOfFoundation,
            self.user.Adresse.streetAddress,
            self.user.Adresse.houseNumber,
            self.user.Adresse.postcode.postcode,
            self.user.Adresse.postcode.village
        )

        self.assertEqual(self.club.clubname, club1.clubname)
        self.assertEqual(self.club.yearOfFoundation, club1.yearOfFoundation)        