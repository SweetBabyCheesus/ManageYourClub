from django.contrib import admin
from django.urls import path, include

from .views import *


urlpatterns = [
    path('addField/', FieldViewOrAdd, name='FieldViewOrAdd'),
    path('showMembershipFormFields/', showFormFieldsView, name='showFormFieldsView'),
    path('membershipFormView/', membershipFormView, name='membershipFormView'),
    path('FileViewOrAdd/', FileViewOrAdd, name='FileViewOrAdd'), 
    path('showFormDataView/', showFormDataView, name='showFormDataView')    
]