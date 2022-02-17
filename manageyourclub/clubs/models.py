# Author: Tobias
from tkinter import CASCADE
from django.db import models
from django_form_builder.models import DynamicFieldMap
import os

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

    @staticmethod
    def create(streetAddress, houseNumber, postcode, village):
        """
        Erstellt ein Adressen-Objekt. 
        Wenn der entsprechende Ort noch nicht in der Datenbank existiert, wird dieser auch erstellt.
        """
        if village:
            postcode, created = PlaceModel.objects.get_or_create(postcode=postcode, village=village)[0]
            if created:
                postcode.save()
    
        AddressModel.objects.create(postcode=postcode, streetAddress=streetAddress, houseNumber=houseNumber).save()
        address = AddressModel.objects.create(postcode=postcode, streetAddress=streetAddress, houseNumber=houseNumber)
        address.save()
        return address

    @staticmethod
    def get_or_create(streetAddress, houseNumber, postcode, village):
        """
        Sucht ein Adressen-Objekt, auf das die übergebenen Parameter zutreffen.
        Wenn das gesuchte Adressen-Objekt nicht gefunden wird, wird es erstellt.
        Für den Parameter postcode soll eine Postleitzahl übergeben werden. Keine Instanz vom PlaceModel.
        """
        postcode, created = PlaceModel.objects.get_or_create(postcode=postcode, village=village)
        if created:
            postcode.save()
        address, created = AddressModel.objects.get_or_create(postcode=postcode, streetAddress=streetAddress, houseNumber=houseNumber)
        if created:
            address.save()
        return address

    def isUsed(self):
        "Prüft ob die Adresse genutzt wird, indem geschaut wird ob es eine Verlinkung zu dieser Adresse gibt."
        return self.clubmodel_set.exists() or self.customuser_set.exists()

class ClubModel(models.Model):
    """
    Model für Vereine. Der primary key ist eine id, die von Django automatisch generiert werden sollte. 
    address ist der foreign key zu AddressModel
    """
    clubname = models.CharField(max_length=30)
    yearOfFoundation = models.CharField(max_length=4)
    address = models.ForeignKey(to=AddressModel, on_delete=models.PROTECT)

    @staticmethod
    def create(clubname, yearOfFoundation, streetAddress, houseNumber, postcode, village):
        """
        Erstellt ein Vereins-Objekt. 
        Wenn die entsprechende Adresse noch nicht in der Datenbank existiert, wird diese auch erstellt.
        """
        address = AddressModel.get_or_create(streetAddress, houseNumber, postcode, village)
            
        club = ClubModel.objects.create(address=address, clubname=clubname, yearOfFoundation=yearOfFoundation)
        club.save()
        return club

    @staticmethod
    def get_or_create(clubname, yearOfFoundation, streetAddress, houseNumber, postcode, village):
        """
        Sucht ein Vereins-Objekt, auf das die übergebenen Parameter zutreffen.
        Wenn das gesuchte Vereins-Objekt nicht gefunden wird, wird es erstellt.
        Für den Parameter postcode soll eine Postleitzahl übergeben werden. Keine Instanz vom PlaceModel.
        """
        address = AddressModel.get_or_create(streetAddress, houseNumber, postcode, village)
            
        club, created = ClubModel.objects.get_or_create(clubname=clubname, yearOfFoundation=yearOfFoundation, address=address)
        if created:
            club.save()
        return club

    def edit(self, clubname, yearOfFoundation, streetAddress, houseNumber, postcode, village):
        """
            Überschreibt die Daten des Objektes mit den übergebenen Parametern.
            Wenn die vorherige Adresse nicht mehr gebraucht wird, wird sie gelöscht.
        """
        self.clubname = clubname
        self.yearOfFoundation = yearOfFoundation
        oldAdr = self.address
        self.address = AddressModel.get_or_create(streetAddress, houseNumber, postcode, village)
        self.save()
        if not oldAdr.isUsed():
            oldAdr.delete()
        return self

    def get_form(self,
                  data=None,
                  files=None,
                  remove_filefields=False,
                  remove_datafields=False,
                  **kwargs):
       """
       Returns the form (empty if data=None)
       if remove_filefields is not False, remove from form the passed FileFields
       if remove_datafields is True, remove all fields different from FileFields
       """
       # retrieve all the fields (the model class is in 'Step 1')
       form_fields_from_model = self.myfieldslistmodel.all().order_by('ordinamento')
       if not form_fields_from_model: return None
       # Static method of DynamicFieldMap that build the constructor dictionary
       constructor_dict = DynamicFieldMap.build_constructor_dict(form_fields_from_model)

       # more params to pass with 'data'
       custom_params = {'extra_1': value_1,
                        'extra_2': value_2}
       # the form retrieved by calling get_form() static method
       form = DynamicFieldMap.get_form(# define it only if you
                                       # need your custom form:
                                       # class_obj=MyDynamicForm,
                                       constructor_dict=constructor_dict,
                                       custom_params=custom_params,
                                       data=data,
                                       files=files,
                                       remove_filefields=remove_filefields,
                                       remove_datafields=remove_datafields)

       return form


class ClubDataModel(models.Model):
    club = models.ForeignKey(to = ClubModel, on_delete=models.CASCADE)
    file_type = models.SmallIntegerField(verbose_name='Art des Dokumentes')
    #field_type 1 = Dokument für Antragsformular
    #TODO: Modell für file_Types implementieren
    data = models.FileField(upload_to='club_data')

    def createMembershipRequestData(club,data):
        #Speichert Daten die im Antragsformular zum Download bereit gestellt werden sollen
        data = ClubDataModel.objects.create(club = club, file_type = 1, data = data)
        return data

    def filename(self):
        return os.path.basename(self.file.name)