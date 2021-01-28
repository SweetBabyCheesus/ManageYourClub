from django import forms
from teams.models import SportModel, TeamModel
from users.models import CustomUser
from members.models import Membership

class TeamForm(forms.ModelForm):
    #Author: Max
    teamName = forms.CharField(max_length=30, label='Mannschaftsname')
    sportName = forms.CharField(max_length=30, label='Sportart')

    class Meta:
        model = TeamModel
        #Felder die ganz normal aus dem Form in die Model-Instanz übernommen werden können 
        fields = ['teamName', 'sportName']

    def SetInstanceID(self, instanceID): # Wird beim Überschreiben von Datensätzen benötigt
        self.pk = instanceID
        return self.pk

    def save(self, club, commit=True):
        """speichert die vom Nutzer eingegebenen Daten"""
        pk = self.pk

        if pk is None: # Wenn der primary key nicht gesetzt wurde, soll ein Objekt hinzugefügt werden.
            instance = super().save(commit=False) # Objekt erstellen

        else: # Wenn der primary key gesetzt wurde, soll ein Objekt geändert werden.
            instance = TeamModel.objects.get(pk=pk) # Objekt holen

            oldSport = instance.sportId
            instance.teamName = self.cleaned_data['teamName'] # Diese Beiden Aktionen werden im ersten Fall automatisch ausgeführt.
            
        instance.clubId = club

        valueSportName = self.cleaned_data['sportName'] 
        
        if club is not None: 
            #Mannschaftserstellung nur möglich, wenn Verein ausgewählt

            sport, created = SportModel.objects.get_or_create(sportName=valueSportName)
            if created and commit:
                sport.save()

            #Jetzt existiert die Sportart in der Datenbank.
            #speichere den Sport im Feld sportId vom TeamModel ab.
            #instance.sportId = SportModell.objects.get(sportName=valueSportName)
            instance.sportId = sport
            if commit:
                instance.save()
                # gegebenenfalls aufräumen
                if pk is not None and not TeamModel.objects.filter(sportId=oldSport).exists(): # gegebenenfalls nicht mehr gebrauchte Adresse löschen
                    oldSport.delete()
            return instance
    

class AddTeamMemberForm(forms.Form):
    #Autor: Max
    #Mailadresse wird genutzt, um Nutzer zu identifizieren. 
    eMail = forms.CharField(max_length=50, label='E-Mail-Adresse')

    def addMember(self, club, team, commit=True):

        eMail = self.cleaned_data['eMail']
        #Bughandling: nur Mitglieder des Vereins sind zu Mannschaften hinzufügbar
        if CustomUser.objects.filter(email=eMail).exists():
            user = CustomUser.objects.get(email=eMail)
            member = Membership.objects.get(member = user, club=club )
            if member.club == club:
                team.members.add(member) 


