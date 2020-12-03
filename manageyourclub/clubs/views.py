from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from clubs.forms import AddClubForm
from django.http import HttpResponse


# Create your views here.

class ClubView(generic.CreateView):
    template_name = 'my_club.html'

def AddClubView(request):
    # FIXME den code habe ich von einer Seite übernommen. Muss evtl auch geändert werden
    if request.method == 'POST':
        form = AddClubForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Your review has been taken')
  
    else:
        form = AddClubForm()
        context = {
            'form':form,
        }
    return render(request, 'new_club.html', context)