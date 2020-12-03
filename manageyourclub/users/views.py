from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login

from .forms import CreateUserForm, CreateUserProfileForm

def login_view(request):
    return render(request, 'registration/login.html')

def SignUpView(request):

    if request.method == 'POST':
        
        user_form = CreateUserForm(request.POST)
        profile_form = CreateUserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request,'home.html')

    else:
        user_form = CreateUserForm()
        profile_form = CreateUserProfileForm()

    context  = {'user_form':user_form, 'profile_form':profile_form}
    return  render(request,'registration/signup.html', context)


def home_view(request):
    if request.user.is_authenticated:
        return Trender(request,'home.html')
    return Trender(request,'home.html')