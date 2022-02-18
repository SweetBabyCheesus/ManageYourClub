from django.urls import path

from .views import *

urlpatterns = [
    path('addField/', FieldViewOrAdd, name='FieldViewOrAdd'),
    path('showMembershipFormFields/', showFormFieldsView, name='showFormFieldsView'),
    path('membershipCustomFormView/', membershipFormView, name='membershipFormView'),
    path('FileViewOrAdd/', FileViewOrAdd, name='FileViewOrAdd'), 
    path('showFormDataView/', showFormDataView, name='showFormDataView'),
    path('RequestMembershipView/', RequestMembershipView, name='RequestMembershipView'), 
    path('acceptRequestClub/', acceptRequestMembershipView, name='acceptRequestMembership'),
    path('declineRequestClub/', declineRequestMembershipView, name='declineRequestMembership'),
    path('<int:request_data>/showMembershipRequestToClubView/', showMembershipRequestToClubView, name='showMembershipRequestToClubView'),
]