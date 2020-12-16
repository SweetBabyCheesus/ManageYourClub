from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from users.models import CustomUser

#https://stackoverflow.com/questions/53461410/make-user-email-unique-django/53461823
class CreateCustomUserForm(UserCreationForm):
    GENDER_CHOICES = [
    ('1', 'männlich'),
    ('2', 'weiblich'),
    ('3', 'divers'),
    ]
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    Vorname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Nachname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Geburtstag = forms.CharField(label='Geburtstag (mm/dd/yyyy)', widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Geschlecht = forms.CharField(label='Geschlecht', widget=forms.Select(choices=GENDER_CHOICES))
    Postleitzahl = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))
    Ort = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Straße = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'text'}))
    Hausnummer = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type':'number'}))
      
    password1.label="Passwort"
    password2.label="Passwort bestätigen"
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