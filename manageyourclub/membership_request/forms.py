# Author: Tobias
from cProfile import label
from django import forms

from membership_request.models import FieldsListModel
from clubs.models import ClubDataModel

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
