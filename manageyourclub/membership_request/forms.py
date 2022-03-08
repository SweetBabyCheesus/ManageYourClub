from cProfile import label
from tabnanny import verbose
from django import forms

from membership_request.models import FieldsListModel
from clubs.models import ClubDataModel
from members.models import Membership
from users.models import Gender


class AddFieldForm(forms.ModelForm):
    #Autor: Max Rosemeier
    #Formular für die Eigenschaften eines neuen Formularfeldes

   
    def edit(self, pk):
        #Findet das Formular mit dem übergebenen Primary Key und 
        #überschreibt dessen Daten mit den Daten aus dem Formular.
        
        instance = FieldsListModel.objects.get(pk=pk) # Objekt holen

        return instance.edit(
            self.cleaned_data['name'], 
            self.cleaned_data['field_type'], 
            self.cleaned_data['valore'],
            self.cleaned_data['is_required'],
            self.cleaned_data['aiuto'],
            self.cleaned_data['pre_Text'],
            self.cleaned_data['ordinamento'],
        )

    def create(self,club):
        #Speichert die vom Nutzer eingegebenen Daten
        return FieldsListModel.create(
            club,
            self.cleaned_data['name'], 
            self.cleaned_data['field_type'], 
            self.cleaned_data['value'],
            self.cleaned_data['is_required'],
            self.cleaned_data['help_text'],
            self.cleaned_data['pre_text'],
            self.cleaned_data['ordering'],
        )

    class Meta:
        model = FieldsListModel
        fields = ('name','field_type','value','is_required','help_text','pre_text','ordering')





class AddFileForm(forms.Form):
    #Autor: Max Rosemeier
    #Formular um Dateien von einem Sportverein für den Antragsprozess hochzuladen

    data = forms.FileField()

    def save(club, data):
        #Speichert die vom Nutzer eingegebenen Daten
        data = ClubDataModel.createMembershipRequestData(
            club=club, 
            data=data,
        )
        return data.save()
        

    class Meta:
        model = ClubDataModel
        fields = ('data')





class UnregisteredMembershipForm(forms.ModelForm):
    #Autor: Max Rosemeier
    #Formular für Standard Membership Formularfeldern bei nicht registrierten Bewerbern
    gender = forms.ModelChoiceField(label='Geschlecht', queryset=Gender.objects.all())
    streetAddress = forms.CharField(max_length=20, label='Straße')
    houseNumber = forms.CharField(max_length=5, label='Hausnummer')
    postcode_id = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            #setzt alle Felder des Forms auf required, im Model sind diese als required=False angegeben aufgrund des Datenmodells
            self.fields[key].required = True 
        

    def create(self, club):
        #Speicherung der Antragsdaten
        return Membership.addUnregisteredMembershipRequestData(
                club,
                self.cleaned_data['phone'], 
                self.cleaned_data['first_name'],
                self.cleaned_data['last_name'],
                self.cleaned_data['birthday'],
                self.cleaned_data['gender'],
                self.cleaned_data['postcode_id'],
                self.cleaned_data['streetAddress'],
                self.cleaned_data['houseNumber'],
                self.cleaned_data['village'],
                self.cleaned_data['iban'],
                self.cleaned_data['bank_account_owner'],
            )

    def membershipExist(self,club):
        #Prüfung ob bereits ein Antrag/ eine Mitgliedschaft mit dem identischen Verein und der identischen Person existiert
        membership = Membership.objects.filter(club = club, first_name= self.cleaned_data['first_name'], last_name = self.cleaned_data['last_name'], birthday = self.cleaned_data['birthday'])
        return membership.exists()

    class Meta:
        model = Membership
        fields = ('phone','first_name','last_name','birthday','gender','postcode_id','streetAddress','houseNumber','village','iban', 'bank_account_owner')



class RegisteredMembershipForm(forms.ModelForm):
    #Autor: Max Rosemeier
    #Formular für Standard Membership Formularfeldern bei registrierten Bewerbern

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key in self.fields:
            #setzt alle Felder des Forms auf required, im Model sind diese als required=False angegeben aufgrund des Datenmodells
            self.fields[key].required = True 


    def create(self,user, club):
        #Speicherung der Antragsdaten
        return Membership.addRegisteredMembershipRequestData(
            user,
            club,
            self.cleaned_data['phone'], 
            self.cleaned_data['iban'], 
            self.cleaned_data['bank_account_owner'],
        )


    class Meta:
        model = Membership
        fields = ('phone','iban', 'bank_account_owner')

