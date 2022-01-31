from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from clubs.models import AddressModel

#Test
"""
from django.contrib.auth import get_user_model as User
from django.db.models.signals import post_save
from django.dispatch import receiver
"""
from django.core.mail import send_mail
from manageyourclub.settings import EMAIL_HOST_USER



"""
class Profile(models.Model):
    user = models.OneToOneField(CostumUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User())
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
"""

#Custom User Manager um Custom User zu erstellen
class CustomUserManager(BaseUserManager):
    #Autor: Max
    #Manager zum Handeln des Angepassten Usermodels

    def create_user(self, email, Vorname, Nachname, Geburtstag, Geschlecht, Adresse, password=None):
        #Überschreibung der create_user Methode, damit  die neuen Felder bei einer Nutzererstellung korrekt gespeichert werden

        #Emailadresse= Username, Dater unbedingt Nötig zur Erstellung eines Accounts
        if not email:
            raise ValueError("Eine Emailadresse wird zur Accounterstellung benötigt")

        Adresse = AddressModel.objects.get(pk=Adresse)
        Geschlecht = Gender.objects.get(pk=Geschlecht)

        #Erstellung eines CustomUser Objects
        user = self.model(
            email=self.normalize_email(email),
            Vorname=Vorname,
            Nachname=Nachname,
            Geburtstag=Geburtstag,
            Geschlecht=Geschlecht,
            Adresse=Adresse
        )
        user.set_password(password)

        #speicherung des Objects in der DB
        user.save(using=self._db)
        return user



    def create_superuser(self, email, password, Vorname, Nachname, Geburtstag, Geschlecht, Adresse):
        #Überschreibung der create_superuser Methode, damit Superuser mit allen Datenfeldern korret angelegt werden

        #Erstellung eines CustomUser Objects
        user = self.create_user(
            email=self.normalize_email(email),
            Vorname=Vorname,
            Nachname=Nachname,
            Geburtstag=Geburtstag,
            Geschlecht=Geschlecht,
            Adresse=Adresse,
            password=password
        )

        #Anpassung der Berechtigungen
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True

        #speicherung des Objects in der DB
        user.save(using=self._db)
        return user

class Gender(models.Model): # Author: Tobias
    """
        Tabelle in welcher die Geschlechts-Auswahlmöglichkeiten gespeichert werden.
        Die Instanzen werden mithilfe der Datei static/standardValues.sql erstellt.
    """
    gender = models.CharField(max_length=8)

    def __str__(self):
        return self.gender

# Erstellung Customuser
# Email muss unique sein, damit Login mit mail möglich ist
class CustomUser(AbstractBaseUser):
    #Max

    #Erstellung der benötigten Datenfelder
    #Emailfeld fungiert als Username. Daher muss sie Unique sein
    email = models.EmailField(verbose_name='email', max_length = 60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    Vorname = models.CharField(max_length=30)
    Nachname = models.CharField(max_length=30)
    Geburtstag = models.DateField()
    Geschlecht = models.ForeignKey(to=Gender, on_delete=models.PROTECT)
    Adresse = models.ForeignKey(to=AddressModel, on_delete=models.PROTECT)
    email_confirmed = models.BooleanField(default=False)

    # damit der Custom Manager genutzt wird
    objects = CustomUserManager()

    #Festlegung: Email als Usernamefeld nutzten
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['Vorname', 'Nachname', 'Geburtstag', 'Geschlecht', 'Adresse']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms (self, app_label):
        return True

    def email_user(self, *args, **kwargs):
        send_mail(
            args[0],
            args[1],
            EMAIL_HOST_USER,
            [self.email],
            fail_silently=False,
        )

    def editAddress(self, streetAddress, houseNumber, postcode, village): # Author: Tobias
        """
            Überschreibt die Daten des Objektes mit den übergebenen Parametern.
            Wenn die vorherige Adresse nicht mehr gebraucht wird, wird sie gelöscht.
        """
        oldAdr = self.Adresse
        self.saveAddress(streetAddress, houseNumber, postcode, village)
        if not oldAdr.isUsed():
            oldAdr.delete()
        return self

    def saveAddress(self, streetAddress, houseNumber, postcode, village): # Author: Tobias
        """
            Beschreibt die Daten des Objektes mit den übergebenen Parametern.
            Diese Funktion sollte nur Dann benutzt werden, wenn das Objekt noch keine Adresse gespeichert hat.
            Ansonsten sollte editAddress genutzt werden.
        """
        self.Adresse = AddressModel.get_or_create(streetAddress, houseNumber, postcode, village)
        self.save()
        return self
