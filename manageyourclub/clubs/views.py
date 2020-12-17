# Diese Datei wurde von Tobias Wenzel erstellt

from django.shortcuts import render, redirect
from clubs.forms import AddClubForm
from clubs.models import ClubModel, AddressModel
from members.forms import addMember

def allClubs(request):
    context = {
        'clubs': ClubModel.objects.all(),
    }
    if not ClubModel.objects.all().exists():
        return redirect('addclub')
    return render(request, 'all_clubs.html', context)

def selectClub(request):
    context = {
        'club_list': ClubModel.objects.all(),
        'to':'home'
    }
    if not ClubModel.objects.all().exists():
        return redirect('addclub')
    return render(request, 'select_club.html', context)

# Tutorial genutzt: https://www.youtube.com/watch?v=F5mRW0jo-U4&t=1358s (2:58:24)
def clubViewOrAdd(request, club):
    if not ClubModel.objects.filter(pk=club).exists():
        return redirect('addclub')
    
    club = ClubModel.objects.get(pk=club)
    context = {
        'club'     : club,
        'club_list': ClubModel.objects.all(),
        'to'         : 'myclub',
    }
    return render(request, 'my_club.html', context)

# Funktion teilweise übernommen von https://www.askpython.com/django/django-model-forms
# Tutorial genutzt https://www.geeksforgeeks.org/initial-form-data-django-forms/
def addClubView(request, club=None):
    if request.method == 'POST': # Wird nach klicken auf Bestätigungsknopf ausgeführt
        form = AddClubForm(request.POST)
        if form.is_valid():
            form.SetInstanceID(club)
            created = club is None
            club = form.save()
            if created:
                addMember(eMail=request.user.email, club=club)
            return redirect('myclub', club.pk)
  
    else:
        if club is None:
            instance = None
            initial = {}
        else: 
            if not ClubModel.objects.filter(pk=club).exists():
                return redirect('addclub')
            instance = ClubModel.objects.get(pk=club)
            initial = {
                'streetAddress' : instance.address.streetAddress,
                'houseNumber'   : instance.address.houseNumber,
                'postcode'      : instance.address.postcode.postcode,
                'village'       : instance.address.postcode.village
            }
        form = AddClubForm(instance=instance, initial=initial)
        
        context = {
            'form':form,
            'club':instance,
        }
        
        if club is not None:
            return render(request, 'edit_club.html', context)
    return render(request, 'new_club.html', context)

def deleteClubView(request, club):
    club = ClubModel.objects.get(pk=club)
    if request.method == 'POST':
        adr = club.address    
        club.delete()
        if not ClubModel.objects.filter(address=adr).exists():
            pc = adr.postcode
            adr.delete()
            if not AddressModel.objects.filter(postcode=pc).exists():
                pc.delete()
        return redirect('/?Verein_wurde_gelöscht:_'+str(club))
    return redirect('/?Verein_wurde_NICHT_gelöscht:_'+str(club))