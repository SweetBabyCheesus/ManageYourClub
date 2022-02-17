# Author: Tobias
from cProfile import label
from tabnanny import verbose
from django import forms

from membership_request.models import FieldsListModel
from clubs.models import ClubDataModel
from members.models import Membership
from users.models import Gender

# Klasse übernommen und abgeändert von:
# https://www.codesd.com/item/how-to-create-forms-for-the-foreign-key-django.html
class AddFieldForm(forms.ModelForm):
    """ModelForm für Vereine"""

   
    def edit(self, pk):
        """
        Findet das Formular mit dem übergebenen Primary Key und 
        überschreibt dessen Daten mit den Daten aus dem Formular.
        """
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
        """Speichert die vom Nutzer eingegebenen Daten"""
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
    gender = forms.ModelChoiceField(label='Geschlecht', queryset=Gender.objects.all())
    streetAddress = forms.CharField(max_length=20, label='Straße')
    houseNumber = forms.CharField(max_length=5, label='Hausnummer')
    postcode_id = forms.IntegerField(max_value=99999, min_value=0, label='PLZ')
    village = forms.CharField(max_length=20, label='Ort')

    def create(self, club):
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

    class Meta:
        model = Membership
        fields = ('phone','first_name','last_name','birthday','gender','postcode_id','streetAddress','houseNumber','village','iban', 'bank_account_owner')



class RegisteredMembershipForm(forms.ModelForm):


    def create(self,user, club):
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

