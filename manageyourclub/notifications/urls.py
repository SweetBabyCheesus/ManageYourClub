from django.urls import path
from notifications.views import requestNotificationView, acceptRequestMembership, declineRequestMembership

urlpatterns = [
    path('<int:club>/overview/', requestNotificationView, name='requestNotifications'),
    path('acceptRequestClub/', acceptRequestMembership, name='acceptRequestMembership'),
    path('declineRequestClub/', declineRequestMembership, name='declineRequestMembership'),
]