from django import forms
from clubs.models import ClubModel
from clubs.models import AddressModel
from clubs.models import PlaceModel

# bisher nicht in Benutzung - ist im Lernprozess über Forms mit Foreign Keys enstanden
# Klasse übernommen und abgeändert von:
# https://www.codesd.com/item/how-to-create-forms-for-the-foreign-key-django.html
class PlaceForm(forms.ModelForm):
    """ModelForm für Orte"""
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
    class Meta:
        model = PlaceModel
        fields = ('postcode', 'village',)

# bisher nicht in Benutzung - ist im Lernprozess über Forms mit Foreign Keys enstanden
# Klasse übernommen und abgeändert von:
# https://www.codesd.com/item/how-to-create-forms-for-the-foreign-key-django.html
class AddressForm(forms.ModelForm):
    """ModelForm für Adressen"""
    streetAddress = forms.CharField(max_length=20, label='Straße und Hausnummer')
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
    class Meta:
        model = AddressModel
        fields = ('streetAddress',)

    def save(self, commit=True):
        """speichert die vom Nutzer eingegebenen Daten"""
        instance = super().save(commit=False)
        fk = self.cleaned_data['postcode']
        if not PlaceModel.objects.filter(postcode=fk).exists():
            PlaceModel.objects.create(postcode=fk, village=self.cleaned_data['village']).save()
        instance.postcode = PlaceModel.objects.get(pk=fk)
        instance.save(commit)
        return instance

# Klasse übernommen und abgeändert von:
# https://www.codesd.com/item/how-to-create-forms-for-the-foreign-key-django.html
class AddClubForm(forms.ModelForm):
    """ModelForm für Vereine"""
    clubname = forms.CharField(max_length=30, label='Vereinsname')
    yearOfFoundation = forms.CharField(max_length=4, label='Gründungsjahr')
    streetAddress = forms.CharField(max_length=20, label='Straße und Hausnummer')
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
     
    def save(self, commit=True):
        """speichert die vom Nutzer eingegebenen Daten"""
        instance = super().save(commit=False)
        strtAddr = self.cleaned_data['streetAddress'] 
        pc = self.cleaned_data['postcode']
        
        # Prüfe ob die Adresse bereits in der DB existiert.
        if not AddressModel.objects.filter(streetAddress=strtAddr, postcode=pc).exists():
            # Wenn die Adresse nicht existiert, Prüfe ob Ort bereits in der DB existiert.
            if not PlaceModel.objects.filter(postcode=pc).exists():
                # Wenn der Ort nicht existiert, erstelle ihn und speichere ihn in der DB ab.
                PlaceModel.objects.create(postcode=pc, village=self.cleaned_data['village']).save()
            # Wenn die Adresse nicht existiert, erstelle sie und speichere ihn in der DB ab.
            # Dafür wird der Ort verwendet, der evtl. eben erst erstellt wurde.
            AddressModel.objects.create(postcode=PlaceModel.objects.get(pk=pc), streetAddress=strtAddr).save()
        # Jetzt existiert die Adresse in der Datenbank
        # speichere die Adresse im Feld address vom ClubModel ab.
        instance.address = AddressModel.objects.get(postcode=pc, streetAddress=strtAddr)
        instance.save(commit)
        return instance
    
    class Meta:
        model = ClubModel
        # Felder die ganz normal aus dem Form in die Model-Instanz übernommen werden können:
        fields = ('clubname', 'yearOfFoundation',)

