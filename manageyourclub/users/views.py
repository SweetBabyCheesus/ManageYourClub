from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login

from .forms import CreateCustomUserForm

def login_view(request):
    return render(request, 'registration/login.html')

def SignUpView(request):

    if request.method == 'POST':
        
        user_form = CreateCustomUserForm(request.POST)

        if user_form.is_valid():
            
            user = user_form.save()

            #username = user_form.cleaned_data.get('username')
            #email = user_form.cleaned_data.get('email')
            #password = user_form.cleaned_data.get('password1')
            #user = authenticate(username=email, password=password)
            login(request, user)
            return render(request,'home.html')

    else:
        user_form = CreateCustomUserForm()

    context  = {'user_form':user_form}
    return  render(request,'registration/signup.html', context)


def home_view(request):
    if request.user.is_authenticated:
        return TemplateView.as_view(template_name='home.html')(request)
    return redirect(reverse_lazy('login'))