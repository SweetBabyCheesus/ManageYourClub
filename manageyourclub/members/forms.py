# Author: Tobias
from django import forms
from members.models import Membership, MemberFunction
from users.models import CustomUser

# Tutorial genutzt: https://www.tutorialspoint.com/python_data_science/python_date_and_time.htm
class AddClubMemberForm(forms.Form):
    eMail = forms.CharField(max_length=30, label='E-Mail-Adresse')

    def addMember(self, club):
        eMail = self.cleaned_data['eMail']
        user = CustomUser.objects.get(email=eMail)
        return Membership.addMember(club, user)

class editMemberForm(forms.Form):
    memberFunction = forms.ModelChoiceField(label='Funktion', queryset=MemberFunction.objects.all(), required=False)

    def saveChanges(self, memship, commit=True):
        memFunction = self.cleaned_data['memberFunction']
        memship.memberFunction = memFunction
        if commit:
            memship.save()
        return memship

