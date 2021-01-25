from django.db import models
from clubs.models import ClubModel
from members.models import Membership

#Author: Max 
#Vorlage für die Models und daraus entstandenen Forms/ Views ist die Club App/ Rücksprache mit Tobias

class SportModel(models.Model):
    #Modell für die Sportart
    #uid wird von Django vorgsteuert
    sportName = models.CharField(max_length=20)


class TeamModel(models.Model):
    #Manschafts Modell, n Teams zu 1 Verein/Clubs Beziehung -> Foreign key zu Clubs 
    #uid wird von Django vorgsteuert     
    #zwischen Mannschaften und Mitgliedern herscht eine m zu n beziehung => manytomanyfield. https://django.readthedocs.io/en/stable/topics/db/queries.html
   
    teamName = models.CharField(max_length=30)
    clubId = models.ForeignKey(to=ClubModel, on_delete=models.CASCADE)
    sportId = models.ForeignKey(to=SportModel, on_delete=models.CASCADE)
    members = models.ManyToManyField(Membership, related_name="teams")


