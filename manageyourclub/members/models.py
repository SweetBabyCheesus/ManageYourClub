from django.db import models
from users.models import CustomUser
from clubs.models import ClubModel
from datetime import datetime
# Vorgabe der Architekten https://vereinsmanagement.atlassian.net/wiki/spaces/VEREINSMAN/pages/33062915/ERM+f+r+Datenbank+mit+Datentypen


# Create your models here.

class PaymentMethod(models.Model):
    """Die verschiedenen Bezahlmethoden sind hier als Strings abgespeichert."""
    paymentMethodID = models.SmallIntegerField(primary_key=True, unique=True)
    paymentMethod   = models.CharField(max_length=15)
    
    def __str__(self):
        return self.paymentMethod

class MemberFunction(models.Model):
    """Die verschiedenen Funktionen von Mitgliedern sind hier als Strings abgespeichert."""
    functionID  = models.SmallIntegerField(primary_key=True, unique=True)
    function    = models.CharField(max_length=15)
    
    def __str__(self):
        return self.function

class MemberState(models.Model):
    """Die Statusmöglichkeiten von Mitgliedern sind hier als Strings abgespeichert."""
    stateID = models.SmallIntegerField(primary_key=True, unique=True)
    state   = models.CharField(max_length=15)

    def __str__(self):
        return self.state

class Membership(models.Model):
    """Model für das Verbindungsstück zwischen Vereinen und Mitgliedern"""
    club            = models.ForeignKey(to=ClubModel, on_delete=models.CASCADE)
    number          = models.AutoField(primary_key=True, unique=True)
    paymentState    = models.CharField(max_length=10, blank=True, null=True) # später vlt mit default
    paymentMethod   = models.ForeignKey(to=PaymentMethod, on_delete=models.PROTECT, blank=True, null=True)
    memberFunction  = models.ForeignKey(to=MemberFunction, on_delete=models.PROTECT, blank=True, null=True)
    memberState     = models.ForeignKey(to=MemberState, on_delete=models.PROTECT, blank=True, null=True)
    member          = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    memberSince     = models.IntegerField()
    phone           = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        unique_together = ('member', 'club',)

    def addMember(club,user):
        #Autor: Max
        #Methode zum hinzufügen von Mitgliedern zu vereinen. Kann mit Membership.addMember(club=...,user=...) angesprochen werden
        if not Membership.objects.filter(member=user, club=club).exists():
            newMember  = Membership.objects.create(member=user, club=club, memberSince=datetime.today().year)
            newMember.save()

    def club_has_member(self, member):
        #Autor Max
        #in Klasse kopiert, damit die Methode besser ansprechbar wird
        user = CustomUser.objects.get(email=member)
        return Membership.objects.filter(club=self, member=member).exists()

def club_has_member(club, member):
    return Membership.objects.filter(club=club, member=member).exists()

# Quelle genutzt: https://stackoverflow.com/questions/5123839/fastest-way-to-get-the-first-object-from-a-queryset-in-django
def get_membership(member, club=None):
    """Gibt die Mitlgiedschaft beim angegebenen Verein aus. 
    Wenn kein Verein angegeben wurde, wird die erste Mitgliedschaft 
    des Benutzers ausgegeben, welche gefunden wird.
    Wenn keine Mitgliedschaft mit den entsprechenden Eigenschaften 
    gefunden wurde wird None zurückgegeben."""

    if club is None:
        return Membership.objects.filter(member=member).first()

    return Membership.objects.filter(member=member, club=club).first()