from django.db import models
from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from clubs.models import AddressModel

#Test
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from manageyourclub.settings import EMAIL_HOST_USER



"""
class Profile(models.Model):
    user = models.OneToOneField(CostumUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
"""
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()

#Custom User Manager um Custom User zu erstellen
class CustomUserManager(BaseUserManager):

    #def create_user(self, email, username, password=None):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Eine Emailadresse wird zur Accounterstellung benötigt")

        #if not username: -> Versuch Username zu entfernen
        #    raise ValueError("Ein Username wird zur Accounterstellung benötigt")   -> Versuch Username zu entfernen

        user = self.model(
            email=self.normalize_email(email),
            #username=username -> Versuch Username zu entfernen
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    #def create_superuser(self, email, username, password): -> Versuch Username zu entfernen
    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            #username=username,
            password=password
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


# Auswahlmöglichleiten für Geschlechteigenschaft des Userprofiles
class Gender(models.Model):
    gender = models.CharField(max_length=8)

    def __str__(self):
        return self.gender

# Erstellung Customuser
# Email muss unique sein, damit Login mit mail möglich ist
class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length = 60, unique=True)
    #username = models.CharField(max_length=30, unique=True) -> versuch Username zu entfernen
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)
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

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['username', 'Vorname', 'Nachname', 'Geburtstag', 'Geschlecht', 'Postleitzahl', 'Ort', 'Straße', 'Hausnummer'] -> versuch username zu entfernen
    REQUIRED_FIELDS = ['Vorname', 'Nachname', 'Geburtstag', 'Geschlecht', 'Postleitzahl', 'Ort', 'Straße', 'Hausnummer']

    def __str__(self):
        return self.username
    
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
