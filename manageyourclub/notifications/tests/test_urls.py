# Author: Tobias
# Tutorial genutzt: https://www.youtube.com/watch?v=0MrgsYswT1c&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=2
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from notifications.views import requestNotificationView, acceptRequestMembership, declineRequestMembership

class TestUrls(SimpleTestCase):

    def test_requestNotifications_url_is_resolved(self):
        url = reverse('requestNotifications', args=[1])
        self.assertEqual(resolve(url).func, requestNotificationView)

    def test_acceptRequestMembership_url_is_resolved(self):
        url = reverse('acceptRequestMembership')
        self.assertEqual(resolve(url).func, acceptRequestMembership)

    def test_declineRequestMembership_url_is_resolved(self):
        url = reverse('declineRequestMembership')
        self.assertEqual(resolve(url).func, declineRequestMembership)