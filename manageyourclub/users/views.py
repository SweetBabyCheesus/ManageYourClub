from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import View, UpdateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from clubs.models import ClubModel
from clubs.views import selectClub

from users.tokens import account_activation_token
from users.forms import CreateCustomUserForm, CustomPasswordChangeForm
from users.models import CustomUser


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            #user.profile.email_confirmed = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


def showUserData(request):
    return render(request, 'userData.html')


def login_view(request):
    return render(request, 'registration/login.html')

# Sign Up View
class SignUpView(View):
    form_class = CreateCustomUserForm
    template_name = 'registration/signup.html'
 
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Bitte bestätige deinen ManageYourClub Account'
            message = render_to_string('email/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Bitte bestätige deinen ManageYourClub Account'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})
        
def home_view(request, club=None):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if club is None:
        return selectClub(request)
        
    context = {
        'club': ClubModel.objects.get(pk=club),
        'club_list': ClubModel.objects.all(),
        'to': 'home',
    }

    return render(request, 'home.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('home')