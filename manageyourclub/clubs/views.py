# Diese Datei wurde von Tobias Wenzel erstellt

from django.shortcuts import render, redirect
from clubs.forms import AddClubForm
from clubs.models import ClubModel, AddressModel

# Tutorial genutzt: https://www.youtube.com/watch?v=F5mRW0jo-U4&t=1358s (2:58:24)
def ClubViewOrAdd(request, pk):
    if not ClubModel.objects.filter(pk=pk).exists():
        return redirect('addclub')
    
    obj = ClubModel.objects.get(pk=pk)
    context = {
        'object'     : obj,
        'object_list': ClubModel.objects.all()
    }
    return render(request, 'my_club.html', context)

# Funktion teilweise übernommen von https://www.askpython.com/django/django-model-forms
# Tutorial genutzt https://www.geeksforgeeks.org/initial-form-data-django-forms/
def AddClubView(request, pk=None):
    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = AddClubForm(request.POST)
        if form.is_valid():
            form.SetInstanceID(pk)
            pk = form.save().id
            return redirect('myclub', pk)
  
    else:
        if pk is None:
            instance = None
            initial = {}
        else: 
            if not ClubModel.objects.filter(pk=pk).exists():
                return redirect('addclub')
            instance = ClubModel.objects.get(pk=pk)
            initial = {
                'streetAddress' : instance.address.streetAddress,
                'houseNumber'   : instance.address.houseNumber,
                'postcode'      : instance.address.postcode.postcode,
                'village'       : instance.address.postcode.village
            }
        form = AddClubForm(instance=instance, initial=initial)
        
        context = {
            'form':form,
            'object':instance,
        }
        
        if pk is not None:
            return render(request, 'edit_club.html', context)
    return render(request, 'new_club.html', context)

def DeleteClubView(request, pk):
    club = ClubModel.objects.get(pk=pk)
    if request.method == 'POST':     
        adr = club.address    
        club.delete()
        if not ClubModel.objects.filter(address=adr).exists():
            pc = adr.postcode
            adr.delete()
            if not AddressModel.objects.filter(postcode=pc).exists():
                pc.delete()
        return redirect('/?Verein_wurde_gelöscht:_'+str(pk))   
    return redirect('/?Verein_wurde_NICHT_gelöscht:_'+str(pk))