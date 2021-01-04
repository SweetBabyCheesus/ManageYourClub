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
    streetAddress = forms.CharField(max_length=20, label='Straße')
    houseNumber = forms.CharField(max_length=5, label='Hausnummer')
    postcode = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')
    class Meta:
        model = AddressModel
        fields = ('streetAddress',)

    def save(self, commit=True):
        """speichert die vom Nutzer eingegebenen Daten"""
        instance = super().save(commit=False)
        pc = self.cleaned_data['postcode']
        vil = self.cleaned_data['village']
        place, created = PlaceModel.objects.get_or_create(postcode=pc, village=vil)
        if created and commit:
            place.save()
        instance.postcode = place
        instance.save(commit)
        return instance

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
    pk = None

    def SetInstanceID(self, instanceID): # Wird beim Überschreiben von Datensätzen benötigt
        self.pk = instanceID
        return self.pk
    
    def save(self, commit=True):
        """speichert die vom Nutzer eingegebenen Daten"""
        pk = self.pk
        if pk is None: # Wenn der primary key nicht gesetzt wurde, soll ein Objekt hinzugefügt werden.
            instance = super().save(commit=False) # Objekt erstellen
        else: # Wenn der primary key gesetzt wurde, soll ein Objekt geändert werden.
            instance = ClubModel.objects.get(pk=pk) # Objekt holen

            oldAdr = instance.address # wird zum Aufräumen benötigt.
            instance.clubname = self.cleaned_data['clubname'] # Diese Beiden Aktionen werden im ersten Fall automatisch ausgeführt.
            instance.yearOfFoundation = self.cleaned_data['yearOfFoundation']

        strtAddr = self.cleaned_data['streetAddress'] 
        hN = self.cleaned_data['houseNumber']
        pc = self.cleaned_data['postcode']
        vil = self.cleaned_data['village']
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
        # speichere die Adresse im Feld address vom ClubModel ab.
        #instance.address = AddressModel.objects.get(postcode=place, streetAddress=strtAddr, houseNumber=hN)
        instance.address = adr
        if commit:
            instance.save()
            # gegebenenfalls aufräumen
            if pk is not None and not ClubModel.objects.filter(address=oldAdr).exists(): # gegebenenfalls nicht mehr gebrauchte Adresse löschen
                oldPc = oldAdr.postcode
                oldAdr.delete()
                if not AddressModel.objects.filter(postcode=oldPc).exists(): # gegebenenfalls nicht mehr gebrauchten Ort löschen
                    oldPc.delete()

        return instance
    
    class Meta:
        model = ClubModel
        # Felder die ganz normal aus dem Form in die Model-Instanz übernommen werden können:
        fields = ('clubname', 'yearOfFoundation')

