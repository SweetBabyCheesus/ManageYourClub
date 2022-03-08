import json
import os
from django.core.files.storage import default_storage
from users.models import CustomUser
from users.models import Gender
from clubs.models import AddressModel, PlaceModel
from members.models import Membership

from manageyourclub.settings import BASE_DIR

def getCustomFormData(self, is_registered):
    #Autor: Max Rosemeier
    #schneidet aus den gesendeten Formulardaten die Custom Formulardaten
    #sodass keine redundante speicherung erfolgt

    jsonData = json.loads(self)
    cuttedJson = '{'

    k = 5

    if not is_registered:
        k = 13

    i = 1
    for key in jsonData:
        i=i+1
        if i > k:
            cuttedJson = str(cuttedJson) + str('"') + str(key) + str('"') + str(': ') + str('"') + str(jsonData[key]) + str('"')

            if i < len(jsonData)+1:
                cuttedJson = cuttedJson + str(', ') 
    
    cuttedJson = cuttedJson + '}'

    return cuttedJson


def saveToMedia(files, membershipId):
    #Autor: Max Rosemeier
    #https://stackoverflow.com/questions/26274021/simply-save-file-to-folder-in-django

    #  Saving POST'ed files to storage
    for file in files:
        file_name = os.path.join(BASE_DIR,'media/membership_request_data/') + str(membershipId) + '_' + str(files[file].name)
        default_storage.save(file_name, files[file])

def getApplicantData(membership, isRegistrated):
    membership_form_Data = [[0 for i in range(2)] for j in range(10)]

    #Der Namen für das Datenfeld an der Oberfläche wird mit dem verbose_name der Felder im Model definiert
    membership_form_Data[0][0] = Membership._meta.get_field('first_name').verbose_name
    membership_form_Data[1][0] = Membership._meta.get_field('last_name').verbose_name
    membership_form_Data[2][0] = Membership._meta.get_field('birthday').verbose_name
    membership_form_Data[3][0] = Gender._meta.get_field('gender').verbose_name
    membership_form_Data[4][0] = Membership._meta.get_field('iban').verbose_name
    membership_form_Data[5][0] = Membership._meta.get_field('bank_account_owner').verbose_name
    membership_form_Data[6][0] = AddressModel._meta.get_field('streetAddress').verbose_name
    membership_form_Data[7][0] = AddressModel._meta.get_field('houseNumber').verbose_name
    membership_form_Data[8][0] = PlaceModel._meta.get_field('postcode').verbose_name
    membership_form_Data[9][0] = PlaceModel._meta.get_field('village').verbose_name

    if isRegistrated:
        #Daten holen für registrierte Anwender, Die Daten sind hier im CustomUser Modell gespeichert
        applicant_user = CustomUser.objects.get(email = membership.member)
        adress = applicant_user.Adresse
        place = adress.postcode
        gender_name = applicant_user.Geschlecht.gender
        
        membership_form_Data[0][1] = applicant_user.Vorname
        membership_form_Data[1][1] = applicant_user.Nachname
        membership_form_Data[2][1] = applicant_user.Geburtstag
        membership_form_Data[3][1] = gender_name
        membership_form_Data[4][1] = membership.iban
        membership_form_Data[5][1] = membership.bank_account_owner

        membership_form_Data[6][1] = adress.streetAddress
        membership_form_Data[7][1] = adress.houseNumber
        membership_form_Data[8][1] = place.postcode
        membership_form_Data[9][1] = place.village


    else: 
        #Daten holen für unregistrierte Anwender, Die Daten sind hier im Membership Modell gespeichert
        gender_name = membership.gender.gender
        adress = membership.adresse
        place = adress.postcode

        membership_form_Data[0][1] = membership.first_name
        membership_form_Data[1][1] = membership.last_name
        membership_form_Data[2][1] = membership.birthday
        membership_form_Data[3][1] = gender_name
        membership_form_Data[4][1] = membership.iban
        membership_form_Data[5][1] = membership.bank_account_owner

        membership_form_Data[6][1] = adress.streetAddress
        membership_form_Data[7][1] = adress.houseNumber
        membership_form_Data[8][1] = place.postcode
        membership_form_Data[9][1] = place.village

    return membership_form_Data