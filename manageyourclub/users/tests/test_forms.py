from users.forms import EditProfileForm, UserDeleteForm, CustomPasswordChangeForm, CreateCustomUserForm
from django.test import TestCase, Client
from users.models import CustomUser, Gender
from clubs.tests.test_views import logTestClientIn

def createGenders():
    Gender.objects.create(gender='männlich')
    Gender.objects.create(gender='weiblich')
    Gender.objects.create(gender='divers')


class TestForms(TestCase):

    def test_CustomPasswordChangeForm_is_valid(self): # Author: Tobias
        """
            Testinhalt:
            Sollte True zurückgeben, wenn
             - das alte Passwort korrekt eingegeben wurde
             - und das neue Passwort die Kriterien für Passwörter (nicht zu kurz, etc. ) einhält
             - und das neue Passwort zweimal gleich eingegeben wurde
            Ansonsten sollte False zurückgegeben werden.
        """
        self.client = Client()
        logTestClientIn(self.client)

        password = 'HariB0M8'
        form = CustomPasswordChangeForm(self.client.user, data={
            'old_password':'12345', 
            'new_password1':password, 
            'new_password2':password, 
        })
        self.assertTrue(form.is_valid())

        password = 'password' # Passwort zu einfach
        form = CustomPasswordChangeForm(self.client.user, data={
            'old_password':'12345', 
            'new_password1':password, 
            'new_password2':password, 
        })
        self.assertFalse(form.is_valid())

        password = 'B0M8' # Passwort zu kurz
        form = CustomPasswordChangeForm(self.client.user, data={
            'old_password':'12345', 
            'new_password1':password, 
            'new_password2':password, 
        })
        self.assertFalse(form.is_valid())

    def test_CreateCustomUserForm_is_valid(self): # Author: Tobias
        """
            Testinhalt:
            Sollte True zurückgeben, wenn alle Daten ordnungsgemäß eingetragen wurden.
            Ansonsten sollte False zurückgegeben werden.
        """
        
        createGenders()

        password = 'HariB0M8'

        form = CreateCustomUserForm(data={
            'password1':password,
            'password2':password,
            'Vorname':'Test',
            'Nachname':'User',
            'email':'manageyourclub@web.de',
            'Geburtstag':'2000-01-01',
            'Geschlecht':2,
            'Straße':'Sesamstraße',
            'Hausnummer':1,
            'Postleitzahl':65199,
            'Ort':'Kuchenhausen',
        })

        # Das Formular ist richtig ausgefüllt
        self.assertTrue(form.is_valid())

        form = CreateCustomUserForm(data={
            'password1':password,
            'password2':password+'1',
            'Vorname':'Test',
            'Nachname':'User',
            'email':'manageyourclub@web.de',
            'Geburtstag':'2000-01-01',
            'Geschlecht':2,
            'Straße':'Sesamstraße',
            'Hausnummer':1,
            'Postleitzahl':65199,
            'Ort':'Kuchenhausen',
        })

        # Das Formular ist falsch ausgefüllt
        self.assertFalse(form.is_valid())

        form = CreateCustomUserForm(data={
            'password1':password,
            'password2':password,
            'Vorname':'Test',
            'Nachname':'User',
            'email':'manageyourclub@web.de',
            'Geburtstag':'2000-01-01',
            'Geschlecht':'a',
            'Straße':'Sesamstraße',
            'Hausnummer':1,
            'Postleitzahl':65199,
            'Ort':'Kuchenhausen',
        })

        # Das Formular ist falsch ausgefüllt
        self.assertFalse(form.is_valid())

    def test_CreateCustomUserForm_save(self): # Author: Tobias
        """
            Testinhalt:
            Es sollte ein Nutzer mit den Im Formular übergebenen Daten erstellt werden.
        """
        
        createGenders()

        password = 'HariB0M8'

        data={
            'password1':password,
            'password2':password,
            'Vorname':'Test',
            'Nachname':'User',
            'email':'manageyourclub@web.de',
            'Geburtstag':'2000-01-01',
            'Geschlecht':2,
            'Straße':'Sesamstraße',
            'Hausnummer':'1',
            'Postleitzahl':'65199',
            'Ort':'Kuchenhausen',
        }

        form = CreateCustomUserForm(data=data)
        self.assertTrue(form.is_valid())

        user = form.save()

        self.assertIsNotNone(user)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.Vorname, data['Vorname'])
        self.assertEqual(user.Nachname, data['Nachname'])
        self.assertEqual(str(user.Geburtstag), data['Geburtstag'])
        self.assertEqual(user.Geschlecht, Gender.objects.get(pk=data['Geschlecht']))
        self.assertEqual(user.Adresse.streetAddress, data['Straße'])
        self.assertEqual(user.Adresse.houseNumber, data['Hausnummer'])
        self.assertEqual(user.Adresse.postcode.postcode, data['Postleitzahl'])
        self.assertEqual(user.Adresse.postcode.village, data['Ort'])

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
       
