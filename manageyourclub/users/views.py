from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

def login_view(request):
    return render(request, 'registration/login.html')

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return TemplateView.as_view(template_name='home.html')(request)
    return redirect(reverse_lazy('login'))