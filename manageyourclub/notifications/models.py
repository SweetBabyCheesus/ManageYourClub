from django.db import models
from users.models import CustomUser
from clubs.models import ClubModel
from django.utils import timezone
from members.models import Membership

class MembershipRequest(models.Model):
    #Autor: Max
    #Table um Mitgliedschaftsanfagen seitens eines Vereins zu verwalten. Das Feld direction gibt an ob der 
    # Verein eine Einladung verschickt hat, oder ein user einer Anfrage
    #https://www.youtube.com/watch?v=hyJO4mkdwuM&t=391s

    user                = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, related_name="user")
    club                = models.ForeignKey(to=ClubModel, on_delete=models.CASCADE, related_name="club")
    #direction 0 = Fehler, 1= User zu Verein, 2 = Verein zu User
    direction           = models.IntegerField(blank=False, null=False)
    #status 0 = Fehler, 1=versendet, 2=angenommen, 3= abgelehnt -> Default bei Erstellung ist der Status versendet (1)
    status              = models.IntegerField(default=1)
    timestamp           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "user: " + self.user.email + ", club: " + self.club.clubname

    def addRequest(user,club,direction):
        #Autor: Max
        #Methode zur Erstellung von Beitrittsanfragen
        if not MembershipRequest.objects.filter(user=user, club=club, direction=direction, status=1).exists():
            if not Membership.objects.filter(member=user, club=club).exists():
                newRequest  = MembershipRequest.objects.create(user=user, club=club, direction=direction)
                newRequest.save()

    def setStatusAccepted(self):
        #Autor: Max
        #Methode um den Status auf angenommen zusetzen. -> DRY Pattern
        self.status = 2
        self.save()

    def setStatusDeclined(self):
        #Autor: Max
        #Methode um den Status auf abgelehnt zusetzen. -> DRY Pattern
        self.status = 3
        self.save()