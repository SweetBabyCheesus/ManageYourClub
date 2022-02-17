import json
import os
from django.core.files.storage import default_storage

from manageyourclub.settings import BASE_DIR

def getCustomFormData(self, is_registered):
    #Autor: Max
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
    #Autor: Max
    #https://stackoverflow.com/questions/26274021/simply-save-file-to-folder-in-django

    #  Saving POST'ed files to storage
    for file in files:
        file_name = os.path.join(BASE_DIR,'media/membership_request_data/') + str(membershipId) + '_' + str(files[file].name)
        default_storage.save(file_name, files[file])