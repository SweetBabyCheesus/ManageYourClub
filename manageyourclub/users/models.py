from django.db import models
from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser


#Manager für nutzer mit email ist unique
class CustomUserManager(BaseUserManager):
    def create_user(self,username, email, password):
        
        #Creates and saves a User with the given email, date of
        #birth and password.
        
        if not email:
            raise ValueError('Users must have an email address')

        if not username:
            raise ValueError('Users must have an username')
        
        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            usnername,
            email=self.normalize_email(email),
            password = password
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        
        #Creates and saves a superuser with the given email, date of
        #birth and password.
        
        user = self.create_user(
            usnername,
            email=self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



# Erstellung Customuser
# Email muss unique sein, damit Login mit mail möglich ist
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()


# Auswahlmöglichleiten für Geschlechteigenschaft des Userprofiles
GENDER_CHOICES = [
    ('1', 'männlich'),
    ('2', 'weiblich'),
    ('3', 'divers'),
    ]

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    Vorname = models.CharField(max_length=100)
    Nachname = models.CharField(max_length=100)
    Geburtstag = models.DateField()
    Geschlecht = models.CharField(max_length=6, choices=GENDER_CHOICES, default='1')
    Postleitzahl = models.IntegerField()
    Ort = models.CharField(max_length=100)
    Straße = models.CharField(max_length=100)
    Hausnummer = models.IntegerField()

