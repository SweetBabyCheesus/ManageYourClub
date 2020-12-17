from django.db import models

# Vorgabe von den Architekten:
# https://vereinsmanagement.atlassian.net/wiki/spaces/VEREINSMAN/pages/33062915/ERM+f+r+Datenbank+mit+Datentypen 
# zum Verständnis von Models genutzt https://www.youtube.com/watch?v=F5mRW0jo-U4&t=1358s

class PlaceModel(models.Model):
    """Model für Orte. Mit einer automatisch generierten ID als primary key"""
    postcode = models.IntegerField()
    village = models.CharField(max_length=20)

class AddressModel(models.Model):
    """
    Model für Adressen. Mit einer automatisch generierten ID als primary key. 
    postcode ist der foreign key zu PlaceModel
    """
    streetAddress = models.CharField(max_length=20)
    houseNumber = models.CharField(max_length=5)
    postcode = models.ForeignKey(to=PlaceModel, on_delete=models.PROTECT)

class ClubModel(models.Model):
    """
    Model für Vereine. Der primary key ist eine id, die von Django automatisch generiert werden sollte. 
    address ist der foreign key zu AddressModel
    """
    clubname = models.CharField(max_length=30)
    yearOfFoundation = models.CharField(max_length=4)
    address = models.ForeignKey(to=AddressModel, on_delete=models.PROTECT)
