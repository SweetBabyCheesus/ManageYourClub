from django.db import models

# Vorgabe von den Architekten:
# https://vereinsmanagement.atlassian.net/wiki/spaces/VEREINSMAN/pages/33062915/ERM+f+r+Datenbank+mit+Datentypen 

# Model für Orte. mit PLZ/postcode als primary key
class PlaceModel(models.Model):
    postcode = models.IntegerField(
        primary_key = True, 
        unique      = True, 
        null        = False, 
        blank       = False
    )
    village = models.CharField(max_length=20, null=False, blank=False)

# Model für Adressen. Der pk ist eine id, die automatisch generiert werden sollte. postcode ist der foreign key zu PlaceModel
class AddressModel(models.Model):
    streetAddress = models.CharField(max_length=20, null=False, blank=False)
    postcode = models.ForeignKey(to=PlaceModel, on_delete=models.PROTECT)

# Model für Vereine. Auch hier ist der pk eine id. address ist der foreign key zu AddressModel
class ClubModel(models.Model):
    clubname = models.CharField(max_length=30, null=False, blank=False)
    yearOfFoundation = models.CharField(max_length=4, null=False, blank=False)
    address = models.ForeignKey(to=AddressModel, on_delete=models.PROTECT, null=False, blank=False)
