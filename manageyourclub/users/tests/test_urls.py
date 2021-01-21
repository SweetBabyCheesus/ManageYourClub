from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

#import der users app views
from users.views import SignUpView, showUserData, deleteuser, edit_profile, home_view, CustomPasswordChangeView, SignUpView

class TestUserUrls(SimpleTestCase):
    #Autor: Max
    #Klasse um die URL's der users app zu testen
    #Tutorial: https://www.youtube.com/watch?v=0MrgsYswT1c&t=46s

    def test_signup_url_is_resolved(self):
        url         =  reverse('signup')
        self.assertEquals(resolve(url).func.view_class, SignUpView)

    def test_home_url_is_resolved(self):
        url         =  reverse('home')
        self.assertEquals(resolve(url).func, home_view)
    
    def test_password_url_is_resolved(self):
        url         =  reverse('password')
        self.assertEquals(resolve(url).func.view_class, CustomPasswordChangeView)

    def test_userData_url_is_resolved(self):
        url         =  reverse('userData')
        self.assertEquals(resolve(url).func, showUserData)
    
    def test_reset_password_url_is_resolved(self):
        url         =  reverse('reset_password')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_password_reset_done_url_is_resolved(self):
        url         =  reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_complete_url_is_resolved(self):
        url         =  reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    def test_deleteuser_url_is_resolved(self):
        url         =  reverse('deleteuser')
        self.assertEquals(resolve(url).func, deleteuser)

    def test_edit_profile_url_is_resolved(self):
        url         =  reverse('edit_profile')
        self.assertEquals(resolve(url).func, edit_profile)

#Account Aktivierung und Passwort reset werden aufgrund der Tokens über Frontend getestet. (Max)