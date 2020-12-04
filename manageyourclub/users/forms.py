from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import UserProfile
#https://stackoverflow.com/questions/53461410/make-user-email-unique-django/53461823
class CreateUserForm(UserCreationForm): 
    class Meta:
        model = User 
        fields = ['username','email','password1','password2']

        def clean(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError("Email exists")
            return self.cleaned_data

        def save(self, commit=True):
            user = super().save(commit=False)

            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()
            return user

class CreateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Vorname', 'Nachname','Geburtstag','Geschlecht','Postleitzahl','Ort','Straße','Hausnummer']