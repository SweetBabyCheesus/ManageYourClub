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
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "registration/reset_password.html"), name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "registration/password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "registration/password_reset_confirm.html"), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "registration/password_reset_done.html"), name ='password_reset_complete')

]