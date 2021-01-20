from django.test import SimpleTestCase
from django.urls import reverse, resolve
from clubs.views import addClubView, clubViewOrAdd, editClubView, deleteClubView, allClubs, requestMembershipView

#Author Jonas
#Tutorial: https://www.youtube.com/watch?v=0MrgsYswT1c&ab_channel=TheDumbfounds
class TestUrls(SimpleTestCase):

    def test_addclub_url_is_resolved(self):
        url = reverse('addclub')
        self.assertEqual(resolve(url).func, addClubView)

    def test_myclub_url_is_resolved(self):
        url = reverse('myclub', args=['1'])
        self.assertEqual(resolve(url).func, clubViewOrAdd)

    def test_editclub_url_is_resolved(self):
        url = reverse('editclub', args=['1'])
        self.assertEqual(resolve(url).func, editClubView)

    def test_deleteclub_url_is_resolved(self):
        url = reverse('deleteclub', args=['1'])
        self.assertEqual(resolve(url).func, deleteClubView)      

    def test_allclubs_url_is_resolved(self):
        url = reverse('allclubs')
        self.assertEqual(resolve(url).func, allClubs)

    def test_requestMembership_url_is_resolved(self):
        url = reverse('requestMembership')
        self.assertEqual(resolve(url).func, requestMembershipView)   