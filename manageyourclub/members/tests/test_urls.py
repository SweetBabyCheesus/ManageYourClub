from django.test import SimpleTestCase
from django.urls import reverse, resolve
from members.views import clubMembersView, editMemberView

#Author Jonas
#Tutorial: https://www.youtube.com/watch?v=0MrgsYswT1c&ab_channel=TheDumbfounds
class TestUrls(SimpleTestCase):

    def test_club_members(self):
        url = reverse('club_members', args=['1'])
        self.assertEqual(resolve(url).func, clubMembersView)

    def test_edit_members(self):
        url = reverse('edit_member', args=[1, 1])
        self.assertEqual(resolve(url).func, editMemberView)
