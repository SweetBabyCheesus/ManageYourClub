from django.test import SimpleTestCase
from clubs.forms import AddClubForm

class TestForms(SimpleTestCase):

    def test_AddClubFormTrue(self):
        form = AddClubForm(data={
            'clubname' : 'fcbayern',
            'yearOfFoundation' : '1900',
            'streetAddress' : 'Teststraße',
            'houseNumber' : '200',
            'postcode' : 12345,
            'village' : 'münchen'
        })

        self.assertTrue(form.is_valid())

    def test_AddClubFormFalse0(self):
        form = AddClubForm(data={})

        self.assertFalse(form.is_valid())            


    def test_AddClubFormFalse1(self):
        form = AddClubForm(data={
            'clubname' : 'fcbayern',
            'yearOfFoundation' : '19200',
            'streetAddress' : 'Teststraße',
            'houseNumber' : '200',
            'postcode' : 12345,
            'village' : 'münchen'
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_AddClubFormFalse2(self):
        form = AddClubForm(data={
            'clubname' : 'fcbayern',
            'yearOfFoundation' : '1920',
            'streetAddress' : 'Teststraße',
            'houseNumber' : '20000000',
            'postcode' : 12345,
            'village' : 'münchen'
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_AddClubFormFalse3(self):
        form = AddClubForm(data={
            'clubname' : 'fcbayernnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
            'yearOfFoundation' : '1920',
            'streetAddress' : 'Teststraße',
            'houseNumber' : '200',
            'postcode' : 'abcde',
            'village' : 'münchen'
        })

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)                  