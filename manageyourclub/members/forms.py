from django import forms
from members.models import Member, Membership
from users.models import CustomUser
from datetime import datetime

# Tutorial genutzt: https://www.tutorialspoint.com/python_data_science/python_date_and_time.htm
class AddClubMemberForm(forms.Form):
    eMail = forms.CharField(max_length=30, label='E-Mail-Adresse')

    def addMember(self, club, commit=True):
        eMail = self.cleaned_data['eMail']
        return addMember(eMail, club, commit)

def addMember(eMail, club, commit=True):
    user = CustomUser.objects.get(email=eMail)
    member = Member.objects.get_or_create(user=user, memberSince=datetime.today().year)[0]
    membership = Membership.objects.create(club=club, member=member)

    if commit:
        member.save()
        membership.save()

    return (member, membership)

class editMemberForm(forms.Form):
    memFunction = forms.CharField(max_length=30)

    #def saveChanges(self, memship, commit=True):
    #    memFunction = self.cleaned_data['memFunction']
        # return saved object

"""
# Seite genutzt: https://docs.djangoproject.com/en/3.1/ref/forms/widgets/
class DeleteClubMemberForm(forms.Form):
    membershipID = forms.IntegerField(widget=forms.HiddenInput())

    def deleteMember(self, commit=True):
        membership = self.cleaned_data['membershipID']
        membership = Membership.objects.get(membership)
        if commit:
            membership.delete()
            return True
        return False
"""