from django.db import models
from clubs.models import ClubModel

""" Author: Max 
Vorlage für die Models und daraus entstandenen Forms/ Views ist die Club App/ Rücksprache mit Tobias"""

class SportModel(models.Model):
    """Modell für die Sportart
    uid wird von Django vorgsteuert"""
    sportName = models.CharField(max_length=20)


class TeamModel(models.Model):
    """Manschafts Modell, n Teams zu 1 Verein/Clubs Beziehung -> Foreign key zu Clubs 
    uid wird von Django vorgsteuert
    """
    teamName = models.CharField(max_length=30)
    clubId = models.ForeignKey(to=ClubModel, on_delete=models.CASCADE)
    sportId = models.ForeignKey(to=SportModel, on_delete=models.CASCADE)
