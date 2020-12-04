from django.db import models
from django import forms
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('1', 'männlich'),
    ('2', 'weiblich'),
    ('3', 'divers'),
    ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Geburtstag = models.DateField()
    Geschlecht = models.CharField(max_length=6, choices=GENDER_CHOICES, default='1')
    Postleitzahl = models.IntegerField()
    Ort = models.CharField(max_length=100)
    Straße = models.CharField(max_length=100)
    Hausnummer = models.IntegerField()

