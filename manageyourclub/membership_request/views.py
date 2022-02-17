from sre_constants import SUCCESS
from django.shortcuts import render
from django.utils.html import strip_tags
from django_form_builder.forms import BaseDynamicForm
from collections import OrderedDict
from django.contrib import messages
from django_form_builder.utils import get_labeled_errors
from django_form_builder.forms import BaseDynamicForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from .utils import *
from members.models import Membership
from membership_request.forms import AddFieldForm
from membership_request.forms import AddFileForm
from membership_request.forms import *
#from membership_request.forms import UnregisteredMembershipForm
from .models import *
from clubs.models import ClubModel, ClubDataModel

def FieldViewOrAdd(request, club):
    #Autor: Max
    #View um individuelle Beitrittsformulare pro Verein zu erstellen
    user = request.user

    if not ClubModel.objects.filter(pk=club).exists():
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        return redirect('allclubs')
        
    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = AddFieldForm(request.POST)
        if form.is_valid():
            form.create(club)
            return redirect('showFormFieldsView', club.pk)
    else:        
        form = AddFieldForm()
        
        context = {
            'club':club,
            'form':form,
        }
        
    return render(request, 'new_Form_Field.html', context)
    

def showFormFieldsView(request,club):
    user = request.user
    club = ClubModel.objects.get(pk=club)

    if not ClubModel.objects.filter(pk=club.id).exists():
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        return redirect('allclubs')
  
    fields = FieldsListModel.objects.filter(club = club)

    context = {
        'club':club,
        'fields': fields,
    }


    return render(request, 'show_Form_Fields.html', context)


def showFormDataView(request,club):
    user = request.user
    club = ClubModel.objects.get(pk=club)

    if not ClubModel.objects.filter(pk=club.id).exists():
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        return redirect('allclubs')
  
    files = ClubDataModel.objects.filter(club = club)

    context = {
        'club':club,
        'files': files,
    }

    return render(request, 'membership_request_Files_list.html', context)


def membershipFormView(request, club):
    user = request.user
    
    if not ClubModel.objects.filter(pk=club).exists():
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        return redirect('MyClub')

    fields = FieldsListModel.objects.filter(club = club)
    constructor_dict = BaseDynamicForm.build_constructor_dict(fields)

    if request.method == 'POST':
        form = BaseDynamicForm.get_form(constructor_dict=constructor_dict,
                                        #data=data,
                                        #files=files,
                                        remove_filefields=False,
                                        remove_datafields=False)
    # if POST (form submitted)
    else:
        form = BaseDynamicForm.get_form(constructor_dict=constructor_dict,
                                        data=request.POST,
                                        files=request.FILES,
                                        remove_filefields=False,
                                        remove_datafields=False)

        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "form is valid")
        else:
            # show all error messages
            for k,v in get_labeled_errors(form).items():
                messages.add_message(request, messages.ERROR,
                                    "<b>{}</b>: {}".format(k, strip_tags(v)))

    context = {
        'form': form,
        'club': club,
        }
    return render(request, "form.html", context)



def FileViewOrAdd(request, club):
    #Autor: Max
    #View um Dateien für Antragsformulare bereitzustellen
    #https://docs.djangoproject.com/en/4.0/topics/http/file-uploads/
    user = request.user

    if not ClubModel.objects.filter(pk=club).exists():
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        return redirect('allclubs')
   
    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = AddFileForm(request.POST, request.FILES)
        if form.is_valid():
            AddFileForm.save(club=club, data=request.FILES['data'])
            return redirect('showFormFieldsView', club.pk)
    else:        
        form = AddFileForm()
        
    context = {
        'form':form,
        'club':club,
    }
        
    return render(request, 'new_File.html', context)






def RequestMembershipView(request, club):
    #Autor: Max
    #Erstellt ein Mitgliedschaftsantragsformular 
    #Zeigt dem Bewerber von Verein Hochgeladene Dateien
    #Fragt Standartfelder ab
    #Fragt Custom Felder ab
    #https://www.codegrepper.com/code-examples/python/Django+two+forms+one+submit

    if not ClubModel.objects.filter(pk=club).exists():
            #falls der Club nicht existiert
            return redirect('allclubs')


    if request.user.is_authenticated:
        #für registrierte User
        user = request.user
        form = RegisteredMembershipForm()

        if Membership.objects.filter(club=club, member = user.id).exists():
            #falls der User bereits Mitglied im Verein ist
            return redirect('allclubs')        

    else:
        #für nicht registrierte User
        form = UnregisteredMembershipForm()


    files = ClubDataModel.objects.filter(club = club)
    club = ClubModel.objects.get(id = club)
    fields = FieldsListModel.objects.filter(club = club)
    constructor_dict = BaseDynamicForm.build_constructor_dict(fields)       
    customForm = BaseDynamicForm()

    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        #Formular für das Membership Model 
        # bei registrierten Nutzern wird ein anderes genutzt als bei unregistrierten
        if request.user.is_authenticated:       
            form = RegisteredMembershipForm(request.POST)
        else:
            form = UnregisteredMembershipForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated: 
                membership = form.create(user,club)
            else:
                membership = form.create(club)

        
        #Formular für Custom Fields
        #Für registrierte und unregistrierte gleich
        #Daten werden in JSON gespeichert
        if FieldsListModel.objects.filter(club = club).exists:
            files=request.FILES
            saveToMedia(files, membership.number)
            
            data=json.dumps(request.POST)
            data = getCustomFormData(data,request.user.is_authenticated)
        
            CustomMembershipData.get_or_create(membership, data)
            
            customForm = BaseDynamicForm.get_form(constructor_dict=constructor_dict,
                                            #data=data,
                                            #files=files,
                                            remove_filefields=False,
                                            remove_datafields=False)
                # if POST (form submitted)
            print(customForm)
            print(form)


    else:
        #Für Membership Modell
        if request.user.is_authenticated:       
            form = RegisteredMembershipForm()
        else:
            form = UnregisteredMembershipForm() 

        #Für Custom Felder
        customForm = BaseDynamicForm.get_form(constructor_dict=constructor_dict,
                                        data=request.POST,
                                        files=request.FILES,
                                        remove_filefields=False,
                                        remove_datafields=False)

        #if not customForm.is_valid():
           # messages.add_message(request, messages.SUCCESS, "OK")
        if customForm.is_valid():
            # show all error messages
            for k,v in get_labeled_errors(customForm).items():
                messages.add_message(request, messages.ERROR,
                                    "<b>{}</b>: {}".format(k, strip_tags(v)))


    context = {
        'form': form,
        'files': files,
        'customForm': customForm,
    }

    return render(request, 'custom_membership_Form.html', context)




"""
https://stackoverflow.com/questions/18489393/django-submit-two-different-forms-with-one-submit-button
if request.method == 'POST':
        form1 = Form1( request.POST,prefix="form1")
        form2 = Form2( request.POST,prefix="form2")
        print(request.POST)
        if form1.is_valid() or form2.is_valid(): 
else:
        form1 = Form1(prefix="form1")
        form2 = Form2(prefix="form2")

"""