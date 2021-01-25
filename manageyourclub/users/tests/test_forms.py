from users.forms import EditProfileForm, UserDeleteForm
from django.test import TestCase
from users.models import CustomUser, Gender

def createGenders():
    Gender.objects.create(gender='männlich')
    Gender.objects.create(gender='weiblich')
    Gender.objects.create(gender='divers')


class TestForms(TestCase):

    def test_EditProfileForm_valid_data(self):
        #Autor Max
        #Test ob EditProfileForm mit korrekten Eingaben funktioniert

        #Geschlechter Tabelle füllen
        createGenders()

        #Füllung des Forms mit korrekten Daten
        form = EditProfileForm(data={
            'Vorname':'Test',
            'Nachname':'User',
            'email':'manageyourclub@web.de',
            'Geschlecht':2,
            'streetAddress':'Sesamstraße',
            'houseNumber':1,
            'postcode':65199,
            'village':'Kuchenhausen',
        })
        #Prüfung ob das Form korrekt gefüllt ist
        self.assertTrue(form.is_valid())        


    def test_EditProfileForm_invalid_data(self):
        #Autor Max
        #Test ob EditProfileForm mit korrekten Eingaben funktioniert

        #Geschlechter Tabelle füllen
        createGenders()

        #Füllung des Forms mit falschen Daten
        form = EditProfileForm(data={
            'Vorname':'Test',
            'Nachname':'User',
            'email':'manageyourclub',#keine korrekte Email
            'Geschlecht':1,
            'streetAddress':'Sesamstraße',
            'houseNumber':1,
            'postcode':65199,
            'village':'Kuchenhausen',
        })
        #Prüfung ob eine Falsche befüllung zum Fehler führt. Ziel: Nur Konsistente Daten sollen übernommen werden
        self.assertFalse(form.is_valid())       

    def test_UserDeleteForm_valid_data(self):
        #Autor Max
        #Test ob UserDeleteForm mit korrekten Eingaben (leer) funktioniert

        #Füllung des Forms mit korrekten Daten
        form = UserDeleteForm(data={})

        #Prüfung ob eine Falsche befüllung zum Fehler führt. Ziel: Nur Konsistente Daten sollen übernommen werden
        self.assertTrue(form.is_valid())       


#Kommentar zu UserDeleteForm (von Max): UserDeleteForm nutzt keine übergebenen Daten. Daher kann es keine Falscheingaben geben.
       
