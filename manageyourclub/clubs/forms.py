# Author: Tobias
from django import forms
from clubs.models import ClubModel
from clubs.models import AddressModel
from clubs.models import PlaceModel

# Klasse übernommen und abgeändert von:
# https://www.codesd.com/item/how-to-create-forms-for-the-foreign-key-django.html
class AddClubForm(forms.ModelForm):
    """ModelForm für Vereine"""
    clubname = forms.CharField(max_length=30, label='Vereinsname')
    yearOfFoundation = forms.CharField(max_length=4, label='Gründungsjahr')
    streetAddress = forms.CharField(max_length=20, label='Straße')
    houseNumber = forms.CharField(max_length=5, label='Hausnummer')
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
    
    def edit(self, pk):
        """
        Findet den Verein mit dem übergebenen Primary Key und 
        überschreibt dessen Daten mit den Daten aus dem Formular.
        """
        instance = ClubModel.objects.get(pk=pk) # Objekt holen

        return instance.edit(
            self.cleaned_data['clubname'], 
            self.cleaned_data['yearOfFoundation'], 
            self.cleaned_data['streetAddress'],
            self.cleaned_data['houseNumber'],
            self.cleaned_data['postcode'],
            self.cleaned_data['village'],
        )

    def create(self):
        """Speichert die vom Nutzer eingegebenen Daten"""
        return ClubModel.create(
            self.cleaned_data['clubname'], 
            self.cleaned_data['yearOfFoundation'], 
            self.cleaned_data['streetAddress'],
            self.cleaned_data['houseNumber'],
            self.cleaned_data['postcode'],
            self.cleaned_data['village']
        )
    
    class Meta:
        model = ClubModel
        # Felder die ganz normal aus dem Form in die Model-Instanz übernommen werden können:
        fields = ('clubname', 'yearOfFoundation')

