from django import forms
from clubs.models import ClubModel
from clubs.models import AddressModel
from clubs.models import PlaceModel
#from django.forms import inlineformset_factory

# ModelForm für Orte
class PlaceForm(forms.ModelForm):
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
    class Meta:
        model = PlaceModel
        fields = ('postcode', 'village',)

# ModelForm für Adressen
class AddressForm(forms.ModelForm):
    streetAddress = forms.CharField(max_length=20, label='Straße und Hausnummer')
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
    class Meta:
        model = AddressModel
        fields = ('streetAddress',)

    def save(self, commit=True):
        instance = super().save(commit=False)
        fk = self.cleaned_data['postcode']
        if not PlaceModel.objects.filter(postcode=fk).exists():
            PlaceModel.objects.create(postcode=fk, village=self.cleaned_data['village']).save()
        instance.postcode = PlaceModel.objects.get(pk=fk)
        instance.save(commit)
        return instance

class AddClubForm(forms.ModelForm):
    clubname = forms.CharField(max_length=30, label='Vereinsname')
    yearOfFoundation = forms.CharField(max_length=4, label='Gründungsjahr')
    streetAddress = forms.CharField(max_length=20, label='Straße und Hausnummer')
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
     

    def save(self, commit=True):
        instance = super().save(commit=False)
        strtAddr = self.cleaned_data['streetAddress'] 
        pc = self.cleaned_data['postcode']
        
        if not AddressModel.objects.filter(streetAddress=strtAddr, postcode=pc).exists(): # wenn nichts gefunden wurde, dann muss das Objekt erstellt werden 
            if not PlaceModel.objects.filter(postcode=pc).exists():
                PlaceModel.objects.create(postcode=pc, village=self.cleaned_data['village']).save()
            AddressModel.objects.create(postcode=PlaceModel.objects.get(pk=pc), streetAddress=strtAddr).save()
        instance.address = AddressModel.objects.get(postcode=pc, streetAddress=strtAddr) # dieses mal sollte die Datenbank die gesuchte adresse gespeichert haben
        instance.save(commit)
        return instance
    
    class Meta:
        model = ClubModel
        fields = ('clubname', 'yearOfFoundation',)

