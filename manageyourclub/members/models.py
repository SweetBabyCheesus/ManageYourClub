# Author: Tobias
from sre_parse import State
from django.db import models
from clubs.models import AddressModel
from users.models import Gender
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
    member          = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE, null=True) #Status der Mitgliedschaft (Beantragt(0), aktiv (1), abgelehnt(2), abgemeldet(3)...)
    memberSince     = models.IntegerField(blank=True, null=True)
    phone           = models.CharField(max_length=20, blank=False, null=True)
    first_name      = models.CharField(max_length=30, blank=False, null=True, verbose_name="Vorname")
    last_name       = models.CharField(max_length=30, blank=False, null=True, verbose_name="Nachname")
    birthday        = models.DateField(blank=True, null=True, verbose_name="Geburtstag")
    adresse         = models.ForeignKey(to=AddressModel, blank=True, null=True, on_delete=models.PROTECT)
    gender          = models.ForeignKey(to=Gender, blank=True, null=True, on_delete=models.PROTECT)
    iban            = models.CharField(max_length=34, blank=True, null=True)
    bank_account_owner = models.CharField(max_length=60, blank=True, null=True)


    class Meta:
        unique_together = ('member', 'club',)

    @staticmethod
    def addMember(club,user):
        #Autor: Max
        #Methode zum hinzufügen von Mitgliedern zu vereinen. Kann mit Membership.addMember(club=...,user=...) angesprochen werden
        if not Membership.objects.filter(member=user, club=club).exists():
            memberState = MemberState.objects.get(stateID = 1)
            newMember  = Membership.objects.create(member=user, club=club, memberSince=datetime.today().year, memberState = memberState)
            newMember.save()
            return newMember
        return None

    @staticmethod
    def addRegisteredMembershipRequestData(user, club, phone, iban, bank_account_owner):
        #Autor: Max
        #Fügt die Daten eines Antragsformulars in den Memberships Table ein
        #Status ist auf 0, die Mitgliedschaft ist somit im Status 'Anfrage' und daher noch nicht aktiv
        if not Membership.objects.filter(member=user, club=club).exists():
            memberState = MemberState.objects.get(stateID = 0)
            newMember  = Membership.objects.create(member=user, club=club, memberState = memberState, phone = phone, iban = iban, bank_account_owner=bank_account_owner )
            newMember.save()
            return newMember
        return None


    @staticmethod
    def addUnregisteredMembershipRequestData(club, phone, first_name, last_name, birthday, gender, postcode_id, streetAddress, houseNumber, village, iban, bank_account_owner):
        #Autor: Max
        #Fügt die Daten eines Antragsformulars in den Memberships Table ein
        #Status ist auf 0, die Mitgliedschaft ist somit im Status 'Anfrage' und daher noch nicht aktiv
        if not Membership.objects.filter(first_name = first_name,last_name=last_name,birthday=birthday, club=club).exists():
            memberState = MemberState.objects.get(stateID = 0)
            adresse = AddressModel.get_or_create(streetAddress, houseNumber, postcode_id, village)
            newMember  = Membership.objects.create(club=club, memberState = memberState, phone = phone, first_name= first_name, last_name = last_name, 
            gender = gender, adresse = adresse, iban = iban, bank_account_owner=bank_account_owner, birthday=birthday)
            newMember.save()
            return newMember
        return None





def club_has_member(club, member):
    return Membership.objects.filter(club=club, member=member, memberState=1).exists()

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