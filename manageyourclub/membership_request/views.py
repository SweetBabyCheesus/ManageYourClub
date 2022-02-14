from sre_constants import SUCCESS
from django.shortcuts import render
from django_form_builder.forms import BaseDynamicForm
from collections import OrderedDict
from django.contrib import messages
from django_form_builder.utils import get_labeled_errors
from django_form_builder.forms import BaseDynamicForm
from django.shortcuts import render, redirect

from members.models import Membership
from membership_request.forms import AddFieldForm
from membership_request.forms import AddFileForm
from membership_request.models import FieldsListModel
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

    if request.method == 'GET':
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

    files = ClubDataModel.objects.get(club = club)    
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
        'files':files,
    }
        
    return render(request, 'new_File.html', context)