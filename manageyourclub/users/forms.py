from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser

#https://stackoverflow.com/questions/53461410/make-user-email-unique-django/53461823
class CreateCustomUserForm(UserCreationForm): 
    class Meta:
        model = CustomUser 
        #fields = ['username','email','password1','password2', 'Vorname', 'Nachname','Geburtstag','Geschlecht','Postleitzahl','Ort','Straße','Hausnummer']
        fields = ['email','password1','password2', 'Vorname', 'Nachname','Geburtstag','Geschlecht','Postleitzahl','Ort','Straße','Hausnummer']


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))

    old_password.label="altes Passwort"
    new_password1.label="neues Passwort"
    new_password2.label="neues Passwort bestätigen"
    class Meta:
        model = CustomUser
    fields = ['old_password','new_password1','new_password2']

"""
warscheinlich durch heutigen fix nicht mehr nötig (10.12.2020)
    # Profile Form
class ProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['username','email']
"""