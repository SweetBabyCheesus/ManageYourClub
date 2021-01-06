from django.db import models
from users.models import CustomUser
from clubs.models import ClubModel
# Vorgabe der Architekten https://vereinsmanagement.atlassian.net/wiki/spaces/VEREINSMAN/pages/33062915/ERM+f+r+Datenbank+mit+Datentypen


# Create your models here.

class PaymentMethod(models.Model):
    """Die verschiedenen Bezahlmethoden sind hier als Strings abgespeichert."""
    paymentMethodID = models.SmallIntegerField(primary_key=True, unique=True)
    paymentMethod   = models.CharField(max_length=15)

class MemberFunction(models.Model):
    """Die verschiedenen Funktionen von Mitgliedern sind hier als Strings abgespeichert."""
    functionID  = models.SmallIntegerField(primary_key=True, unique=True)
    function    = models.CharField(max_length=15)

class MemberState(models.Model):
    """Die Statusmöglichkeiten von Mitgliedern sind hier als Strings abgespeichert."""
    stateID = models.SmallIntegerField(primary_key=True, unique=True)
    state   = models.CharField(max_length=15)

class Member(models.Model):
    """Model für Vereinsmitglieder"""
    user        = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, primary_key=True, unique=True)
    memberSince = models.IntegerField()
    number      = models.IntegerField(blank=True, null=True)
    phone       = models.CharField(max_length=20, blank=True, null=True)

# Tutorial genutzt: https://stackoverflow.com/questions/2201598/how-to-define-two-fields-unique-as-couple
class Membership(models.Model):
    """Model für das Verbindungsstück zwischen Vereinen und Mitgliedern"""
    club            = models.ForeignKey(to=ClubModel, on_delete=models.CASCADE)
    number          = models.AutoField(primary_key=True, unique=True)
    paymentState    = models.CharField(max_length=10, blank=True, null=True) # später vlt mit default
    paymentMethod   = models.ForeignKey(to=PaymentMethod, on_delete=models.PROTECT, blank=True, null=True)
    memberFunction  = models.ForeignKey(to=MemberFunction, on_delete=models.PROTECT, blank=True, null=True)
    memberState     = models.ForeignKey(to=MemberState, on_delete=models.PROTECT, blank=True, null=True)
    member          = models.ForeignKey(to=Member, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        unique_together = ('member', 'club',)

def club_has_member(club, member):
    return Membership.objects.filter(club=club, member=member).exists()

def club_has_user_as_member(club, user):
    member = Member.objects.filter(user=user).first()
    if member is None:
        return False
    return club_has_member(club, member)

# Quelle genutzt: https://stackoverflow.com/questions/5123839/fastest-way-to-get-the-first-object-from-a-queryset-in-django
def get_membership(user, club=None):
    """Gibt die Mitlgiedschaft beim angegebenen Verein aus. 
    Wenn kein Verein angegeben wurde, wird die erste Mitgliedschaft 
    des Benutzers ausgegeben, welche gefunden wird.
    Wenn keine Mitgliedschaft mit den entsprechenden Eigenschaften 
    gefunden wurde wird None zurückgegeben."""
    if not Member.objects.filter(user=user).exists():
        return None
    member = Member.objects.get(user=user)

    if club is None:
        return Membership.objects.filter(member=member).first()

    return Membership.objects.filter(member=member, club=club).first()