from django import forms
from clubs.models import ClubModel
from clubs.models import AddressModel
from clubs.models import PlaceModel
from django.forms import inlineformset_factory

# ModelForm für Orte
class PlaceForm(forms.ModelForm):
    postcode = forms.IntegerField(max_value=99999, min_value=0, required=True, label='PLZ', show_hidden_initial='63842')
    village = forms.CharField(max_length=20, required=True, label='Ort', show_hidden_initial='Bolzhausen')
    class Meta:
        model = PlaceModel
        fields = ('postcode', 'village',)

# ModelForm für Adressen | benötigt noch eine Verbindung zu PlaceForm
class AddressForm(forms.ModelForm):
    streetAddress = forms.CharField(max_length=20, required=True, label='Straße und Hausnummer', show_hidden_initial='Kickerstraße 17')
    class Meta:
        model = AddressModel
        # FIXME PlaceForm einbinden
        fields = ('streetAddress',)

# mein kläglicher Versuch ein funktionierendes Modelform für Vereine zu erstellen:
"""
class AddClubForm(forms.ModelForm):
    clubname = forms.CharField(max_length=30, required=True, label='Vereinsname', show_hidden_initial='Fußballverein Bolzhausen')
    yearOfFoundation = forms.CharField(max_length=4, required=True, label='Gründungsjahr', show_hidden_initial='2010')
     
    def save(self, commit=True):
        instance = super().save(commit=False)
        fk = self.cleaned_data['address']
        instance.address = AddressModel.objects.get(pk=fk)
        instance.save(commit)
        return instance
    
    class Meta:
        model = ClubModel
        # FIXME AddressForm einbinden
        fields = ('clubname', 'yearOfFoundation',)
"""

# https://zenon.cs.hs-rm.de/twenz001/vereinsmanagement/-/issues/14 | Vorgabe von den Architekten
# das Form so wie es aussehen soll (nutzt aber noch nicht die Models):
class AddClubForm(forms.Form):
    clubname = forms.CharField(max_length=30, required=True, label='Vereinsname', show_hidden_initial='Fußballverein Bolzhausen')
    yearOfFoundation = forms.CharField(max_length=4, required=True, label='Gründungsjahr', show_hidden_initial='2010')
    streetAddress = forms.CharField(max_length=20, required=True, label='Staße und Hausnummer', show_hidden_initial='Kickerstraße 17')
    postcode = forms.IntegerField(max_value=99999, min_value=0, required=True, label='PLZ', show_hidden_initial='63842')
    village = forms.CharField(max_length=20, required=True, label='Ort',show_hidden_initial='Bolzhausen')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        fk = self.cleaned_data['address']
        instance.address = AddressModel.objects.get(pk=fk)
        instance.save(commit)
        return instance
        
    class Meta:
        fields = ('clubname', 'yearOfFoundation',)


# keine ahnung ob man das mit inlineformsets schaffen kann 
# AddressFormSet = inlineformset_factory(PlaceModel, AddressModel, AddressForm, fk_name='postcode', can_delete=False)
# AddClubFormSet = inlineformset_factory(AddressModel, ClubModel, AddClubForm, AddressFormSet, 'address', can_delete=False)


