from sre_constants import SUCCESS
from django.shortcuts import render
from django.utils.html import strip_tags
from django_form_builder.forms import BaseDynamicForm
from collections import OrderedDict
from django.contrib import messages
from django_form_builder.utils import get_labeled_errors
from django_form_builder.forms import BaseDynamicForm
from django.shortcuts import render, redirect
import json

from .utils import *
from members.models import Membership, club_has_member
from .forms import *
from .models import *
from clubs.models import ClubModel, ClubDataModel

def FieldAdd(request, club):
    #Autor: Max Rosemeier
    #View um individuelle Beitrittsformulare pro Verein zu erstellen
    user = request.user

    if not ClubModel.objects.filter(pk=club).exists():
        #Prüfung ob der Verein existiert
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        #Berechtigungsprüfung des Users
        return redirect('allclubs')
        
    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': 
        #Wird nach klicken auf Bestätigungsknopf ausgeführt
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
    #Austor: Max Rosemeier
    #Diese View Methode stellt die Custom Membership Formularfelder in einer Übersicht für den Verein bereit
    user = request.user
    club = ClubModel.objects.get(pk=club)

    if not ClubModel.objects.filter(pk=club.id).exists():
        #Prüfung ob gewählter Verein existiert
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        #Prüfung der Berechtigung vom User
        return redirect('allclubs')
  
    fields = FieldsListModel.objects.filter(club = club)

    context = {
        'club':club,
        'fields': fields,
    }


    return render(request, 'show_Form_Fields.html', context)


def showFormDataView(request,club):
    #Autor: Max Rosemeier
    #Dieser View stellt eine Übersicht für die Hochgeladenen Dateien für einen Mitgliedschaftsantrag bereit
    user = request.user
    club = ClubModel.objects.get(pk=club)

    if not ClubModel.objects.filter(pk=club.id).exists():
        #Prüfung ob der Verein existiert
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        #Prüfung der User Berechtigung im Verein
        return redirect('allclubs')
  
    files = ClubDataModel.objects.filter(club = club)

    context = {
        'club':club,
        'files': files,
    }

    return render(request, 'membership_request_Files_list.html', context)




def FileAdd(request, club):
    #Autor: Max Rosemeier Rosemeier
    #View um Dateien für Antragsformulare bereitzustellen
    #https://docs.djangoproject.com/en/4.0/topics/http/file-uploads/
    user = request.user

    if not ClubModel.objects.filter(pk=club).exists():
        #prüfung ob gewählter Verein existiert
        return redirect('allclubs')

    if not Membership.objects.filter(club=club, member = user.id).exists():
        #Berechtigungsprüfung
        return redirect('allclubs')
   
    club = ClubModel.objects.get(pk=club)

    if request.method == 'POST': 
        # Wird nach klicken auf Bestätigungsknopf ausgeführt
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
    #Autor: Max Rosemeier Rosemeier
    #Erstellt ein Mitgliedschaftsantragsformular 
    #Zeigt dem Bewerber von Verein Hochgeladene Dateien
    #Fragt Standartfelder ab
    #Fragt Custom Felder ab
    #https://www.codementor.io/@lakshminp/handling-multiple-forms-on-the-same-page-in-django-fv89t2s3j
    user = request.user

    if not ClubModel.objects.filter(pk=club).exists():
            #falls der Club nicht existiert
            return redirect('allclubs')


    if user.is_authenticated:
        #Definition des Formulars für registrierte User
        form = RegisteredMembershipForm()

        if Membership.objects.filter(club=club, member = user.id).exists():
            #falls der User bereits Mitglied im Verein ist
            return redirect('allclubs')        

    else:
        #Definition des Formulars für nicht registrierte User
        form = UnregisteredMembershipForm()


    files = ClubDataModel.objects.filter(club = club)
    club = ClubModel.objects.get(id = club)
    fields = FieldsListModel.objects.filter(club = club)
    constructor_dict = BaseDynamicForm.build_constructor_dict(fields)       
    customForm = BaseDynamicForm.get_form(constructor_dict=constructor_dict)

    if request.method == 'POST': 
    #Wird nach klicken auf Bestätigungsknopf ausgeführt


        if user.is_authenticated:       
            form = RegisteredMembershipForm(request.POST)
        else:
            form = UnregisteredMembershipForm(request.POST)

        customForm = BaseDynamicForm.get_form(constructor_dict=constructor_dict,
                                                data=request.POST,
                                                files=request.FILES,
                                                remove_filefields=False,
                                                remove_datafields=False)


        if form.is_valid() and customForm.is_valid():
            #Speicherung der Formulardaten, falls die Eingaben korrekt sind

            if not user.is_authenticated:
                if form.membershipExist(club):
                    return redirect('login')

            if user.is_authenticated: 
                membership = form.create(user,club)
            else:
                membership = form.create(club)

        
            if FieldsListModel.objects.filter(club = club).exists:
                #Formular für Custom Fields
                #Für registrierte und unregistrierte Bewerber gleich
                #Daten werden in JSON gespeichert
                
                files=request.FILES
                saveToMedia(files, membership.number)
                
                data=json.dumps(request.POST)
                data = getCustomFormData(data,request.user.is_authenticated)
            
                CustomMembershipData.get_or_create(membership, data) 
            
            if request.user.is_authenticated:
            #weiterleitung nachdem die Eingaben des Bewerbers gespeichert wurden
                return redirect('allclubs')
            else:
                return redirect('login')
    

    context = {
        'form': form,
        'files': files,
        'customForm': customForm,
    }

    return render(request, 'custom_membership_Form.html', context)



def acceptRequestMembershipView(request, request_data, club):
    #Autor: Max Rosemeier
    #Funktion um Mitgliedsanfragen von Usern an Vereine anzunehmen
    #TODO: Anpassen für Thesis
    user = request.user

    if not Membership.objects.filter(member=user.id).exists():
        #Berechtigungsprüfung
        return redirect('home')

    membership = Membership.objects.get(number=request_data)

    if request.method == 'POST':
        #Anpassung der Antragsdaten auf angenommen
        membership.setStatusAccepted()

    return redirect('home')
    


def declineRequestMembershipView(request,club, request_data):
    #Autor: Max Rosemeier
    #Funktion um Mitgliedsanfragen von Usern an Vereine abzulehnen
    #TODO: Anpassen für Thesis
    user = request.user

    if not Membership.objects.filter(member=user.id).exists():
        #Berechtigungsprüfung
        return redirect('home')

    membership = Membership.objects.get(number=request_data)

    if request.method == 'POST': 

        #Anpassung der Antragsdaten auf abgelehnt
        membership.setStatusDeclined()
    return redirect('home')




def showMembershipRequestToClubView(request, club, request_data):
    #Autor: Max Rosemeier
    #Diese Methode zeigt einem Vereinsadmin die Daten einer Beitrittsanfrage
    #In dem Template kann er die Anfrage besttigen oder ablehnen 
    user = request.user
    
    if Membership.objects.filter(club=club, member = user).exists():
    #Nur Vereinsmitglieder können Beitrittsanfragen prüfen
    #Derzeit kein Rollenkonzept innerhalb von Vereinen / muss in Zukunft noch ergänzt werden und die Berechtigungsprüfung muss angepasst werden

        membership = Membership.objects.get(number=request_data)

        if membership.member is None:
            membership_applicant_data = getApplicantData(membership,False)
        else:
            membership_applicant_data = getApplicantData(membership,True)
        
        memberState = membership.memberState

        if memberState.stateID > 0:
            #Falls der Antrag bereits geprüft wurde soll eine 2. Prüfung unterbunden werden
            return redirect('home')

        if CustomMembershipData.objects.filter(membership = membership.number).exists():
            #laden der Custom Membership Daten, sofern diese existieren
            Json_Data = CustomMembershipData.objects.get(membership = membership.number).json

        context = {
            'json': json.loads(Json_Data),
            'membership': membership,
            'membership_applicant_data': membership_applicant_data,
        }


        return render(request,'membershipRequestAnswer.html' ,context)
    

    #Falls User nicht Berechtigt um Anfrage zu prüfen:
    return redirect('allclubs')