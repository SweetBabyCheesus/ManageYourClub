from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
from .models import CustomUser

#https://stackoverflow.com/questions/53461410/make-user-email-unique-django/53461823
class CreateCustomUserForm(UserCreationForm): 
    class Meta:
        model = CustomUser 
        fields = ['username','email','password1','password2', 'Vorname', 'Nachname','Geburtstag','Geschlecht','Postleitzahl','Ort','Straße','Hausnummer']