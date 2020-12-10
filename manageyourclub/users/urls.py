from django.urls import path

from .views import SignUpView, home_view, CustomPasswordChangeView
from django.contrib.auth import views as auth_views
from users.views import SignUpView, ActivateAccount, showUserData


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', home_view, name='home'),
    #Tutorial für Passwortändern: https://www.youtube.com/watch?v=P6QHswl2PqE
    #funktionalitäten stellt Django, in Views file und changePassword.html findet customizing statt
    path('password/', CustomPasswordChangeView.as_view(template_name='registration/changePassword.html'), name='password'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('userdata/', showUserData, name='userData'),
]