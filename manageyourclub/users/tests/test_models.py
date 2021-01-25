# Author: Tobias
from django.test import TestCase
from clubs.tests.test_views import createTestUser
from django.core import mail 
from users.models import CustomUserManager, CustomUser

class TestModels(TestCase):
    
    def setUp(self):
        "Vorbereitung für die Tests"
        self.user = createTestUser()
        self.userManager = CustomUserManager()
        self.userManager.model = CustomUser

    def test_create_user(self):
        """
            Testinhalt:
            Es sollte ein Nutzer mit den Angegebenen Daten erstellt werden.
            Wenn keine E-Mail-Adresse übergeben wurde soll ein Fehler ausgegeben werden.
            Der Nutzer sollte keine besonderen Rechte haben.
        """
        self.assertRaises(
            ValueError,
            self.userManager.create_user,
            '', 
            self.user.Vorname, 
            self.user.Nachname, 
            self.user.Geburtstag, 
            self.user.Geschlecht.pk, 
            self.user.Adresse.pk, 
            self.user.password
        )

        email = 'test3@email.de'
        user = self.userManager.create_user(
            email, 
            self.user.Vorname, 
            self.user.Nachname, 
            self.user.Geburtstag, 
            self.user.Geschlecht.pk, 
            self.user.Adresse.pk, 
            self.user.password
        )
        self.assertIsNotNone(user)

        self.assertEqual(user.email, email)
        self.assertEqual(user.Vorname, self.user.Vorname)
        self.assertEqual(user.Nachname, self.user.Nachname)
        self.assertEqual(user.Geburtstag, self.user.Geburtstag)
        self.assertEqual(user.Geschlecht, self.user.Geschlecht)
        self.assertEqual(user.Adresse, self.user.Adresse)

        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
    def test_create_superuser(self):
        """
            Testinhalt: 
            Der erstellte Nutzer sollte Mitarbeiter- und Adminrechte haben. 
        """
        user = self.userManager.create_superuser(
            'email@email.de', 
            self.user.password,
            self.user.Vorname, 
            self.user.Nachname, 
            self.user.Geburtstag, 
            self.user.Geschlecht.pk, 
            self.user.Adresse.pk
        )

        self.assertTrue(user.is_admin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test__str__(self):
        """
            Testinhalt:
            Es sollte die E-Mail-Adresse des Nutzers zurückgegeben werden.
        """
        self.assertEqual(self.user.email, self.user.__str__())

    def test_has_perm(self):
        """
            Testinhalt:
            Es sollte ein Wahrheitswert zurückgegeben werden, welcher
            bestimmt ob der Nutzer Adminrechte hat.
        """
        self.assertEqual(self.user.has_perm(None), self.user.is_admin)

    def test_has_module_perms(self):
        """
            Testinhalt:
            Sollte Wahr zurückgeben.
        """
        self.assertEqual(self.user.has_module_perms(None), True)

    # Tutorial genutzt: https://timonweb.com/django/testing-emails-in-django/
    def test_email_user(self):
        """
            Testinhalt:
            Es sollte eine E-Mail mit dem übergebenen Inhalt an den Nutzer verschickt werden.
        """
        subject = 'Grüße'
        body = 'Hallo, guten Tag.'
        self.user.email_user(subject, body)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], self.user.email)
        self.assertEqual(mail.outbox[0].subject, subject)
        self.assertEqual(mail.outbox[0].body, body)
        
    def test_editAddress(self): # FIXME Jonas macht das
        """
            Testinhalt:
            Überschreibt bereits vorhandene Adressdaten des Nutzers. 
            Die vorherige Adresse wird, falls ungenutzt, gelöscht, sodass kein 
            Datenmüll entsteht.
        """

    def test_saveAddress(self): # FIXME Jonas macht das
        """
            Testinhalt:
            Das vorher ungenutzte Adressfeld des Nutzers wird ordnungsgemäß ausgefüllt.
        """
