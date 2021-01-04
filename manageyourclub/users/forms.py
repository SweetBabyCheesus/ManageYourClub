from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django import forms
from users.models import CustomUser
from clubs.models import AddressModel, PlaceModel

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

    def save(self, commit=True):
        "speichert die vom Nutzer eingegebenen Daten"
        instance = super().save(commit=False) # Objekt erstellen

        strtAddr = self.cleaned_data['Straße'] 
        hN = self.cleaned_data['Hausnummer']
        pc = self.cleaned_data['Postleitzahl']
        vil = self.cleaned_data['Ort']

        place, created = PlaceModel.objects.get_or_create(postcode=pc, village=vil)
        if created and commit:
            place.save()
            
        adr, created = AddressModel.objects.get_or_create(
            postcode=place, 
            streetAddress=strtAddr, 
            houseNumber=hN
        )
        if created and commit:
            adr.save()

        # Jetzt existiert die Adresse in der Datenbank.
        # speichere die Adresse im Feld Adresse vom CustomUser ab.
        # instance.Adresse = AddressModel.objects.get(postcode=place, streetAddress=strtAddr, houseNumber=hN)
        instance.Adresse = adr
        if commit:
            instance.save()

        return instance


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