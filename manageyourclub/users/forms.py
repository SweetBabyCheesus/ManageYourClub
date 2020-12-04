from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import UserProfile

class CreateUserForm(UserCreationForm): 
    class Meta:
        model = User 
        email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.', widget=(forms.TextInput(attrs={'class': 'form-control'})))
        username = email
        fields = ['first_name','last_name','username','email','password1','password2']

        def save(self, commit=True):
            user = super().save(commit=False)

            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']

            if commit:
                user.save()
            return user

class CreateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['Geburtstag','Geschlecht','Postleitzahl','Ort','Straße','Hausnummer']