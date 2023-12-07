import discord
from discord.ui import View, Button
import datetime
from ics import Calendar
import requests
mois = {
    1 : "Janvier",
    2 : "Février",
    3 : "Mars",
    4 : "Avril",
    5 : "Mai",
    6 : "Juin",
    7 : "Juillet",
    8 : "Août",
    9 : "Septembre",
    10 : "Octobre",
    11 : "Novembre",
    12 : "Décembre",
}

class BtnSemaineSuivante(View):
    def __init__(self, semaine, groupeId, groupeName, heureDecalage, avatar_bor):
        super().__init__()
        self.semaine = semaine
        self.groupeName = groupeName
        self.groupeId = groupeId
        self.heureDecalage =heureDecalage
        self.avatar_bor = avatar_bor

    @discord.ui.button(label="Semaine précedente", style=discord.ButtonStyle.primary)
    async def semainePreBtn(self, interaction:discord.Interaction, button:Button):
        self.semaine[0]["date"] = self.semaine[0]["date"] - datetime.timedelta(days=7)
        self.semaine[1]["date"] = self.semaine[1]["date"] - datetime.timedelta(days=7)
        self.semaine[2]["date"] = self.semaine[2]["date"]  - datetime.timedelta(days=7)
        self.semaine[3]["date"] = self.semaine[3]["date"]  - datetime.timedelta(days=7)
        self.semaine[4]["date"] = self.semaine[4]["date"]  - datetime.timedelta(days=7)
        # Parse the URL
        url = 'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=' + self.groupeId + '&projectId=3&calType=ical&firstDate=' + str(self.semaine[0]["date"].year) + '-' + str(self.semaine[0]["date"].month) + '-' + str(
            self.semaine[0]["date"].day) + '&lastDate=' + str(self.semaine[4]["date"].year) + '-' + str(self.semaine[4]["date"].month) + '-' + str(self.semaine[4]["date"].day)

        try:
            cal = Calendar(requests.get(url).text)
        except Exception as e:
            print(e)
            await interaction.followup.send("Erreur : veuillez réessayer.")
        embed = discord.Embed()
        # Print all the event
        events = cal.events
        sorted_events = sorted(events, reverse=False)
        embed.set_author(name="Emploi du temps des " + self.groupeName)
        embed.description = "Du Lundi " + str(self.semaine[0]["date"].day) + " "+mois[self.semaine[0]["date"].month]+ " au Vendredi " + str(self.semaine[4]["date"].day)+ " "+mois[self.semaine[4]["date"].month]
        for jourjour in self.semaine:

            msg = ""
            for event in sorted_events:
                if self.semaine[jourjour]["date"].day == event.begin.date().day:
                    tmp = event.description.split("\n", 4)[3].split(" ")
                    professeur = ""
                    for i in range(len(tmp)-1):
                        professeur += tmp[i] + " "
                    cours_list = event.name.split(" ")
                    cours = ""
                    if len(cours_list) > 2:
                        del cours_list[0]
                        del cours_list[-1]
                    for caractere in cours_list:
                        cours += caractere + " "
                    heureDeb = event.begin.strftime('%H:%M').split(":")
                    heureFin = event.end.strftime('%H:%M').split(":")
                    vraiheureDeb = int(heureDeb[0]) + self.heureDecalage
                    vraiheureFin = int(heureFin[0]) + self.heureDecalage
                    if vraiheureDeb >= 10:
                        heureDeb = "" + str(vraiheureDeb) + ":" + heureDeb[1]
                        heureFin = str(vraiheureFin) + ":"+ heureFin[1]
                    else:
                        heureDeb = "0" + str(vraiheureDeb) + ":" + heureDeb[1]
                        heureFin = str(vraiheureFin) + ":"+ heureFin[1]
                    msg += "**" + heureDeb + "** -> **"+heureFin+"**: `" + cours + "` " + event.location + " *" + professeur + "*\n"
            
            if msg == "":
                msg = "PAS DE COURS"
            embed.add_field(name=self.semaine[jourjour]["trad"], value=msg, inline=False)
        embed.set_footer(text="Bot crée par Manolo", icon_url=self.avatar_bor)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label="Semaine suivante", style=discord.ButtonStyle.primary)
    async def semaineSuivBtn(self, interaction:discord.Interaction, button:Button):
        self.semaine[0]["date"] = self.semaine[0]["date"] + datetime.timedelta(days=7)
        self.semaine[1]["date"] = self.semaine[1]["date"] + datetime.timedelta(days=7)
        self.semaine[2]["date"] = self.semaine[2]["date"]  + datetime.timedelta(days=7)
        self.semaine[3]["date"] = self.semaine[3]["date"]  + datetime.timedelta(days=7)
        self.semaine[4]["date"] = self.semaine[4]["date"]  + datetime.timedelta(days=7)
        # Parse the URL
        url = 'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=' + self.groupeId + '&projectId=3&calType=ical&firstDate=' + str(self.semaine[0]["date"].year) + '-' + str(self.semaine[0]["date"].month) + '-' + str(
            self.semaine[0]["date"].day) + '&lastDate=' + str(self.semaine[4]["date"].year) + '-' + str(self.semaine[4]["date"].month) + '-' + str(self.semaine[4]["date"].day)

        try:
            cal = Calendar(requests.get(url).text)
        except Exception as e:
            print(e)
            await interaction.followup.send("Erreur : veuillez réessayer.")
        embed = discord.Embed()
        # Print all the event
        events = cal.events
        sorted_events = sorted(events, reverse=False)
        embed.set_author(name="Emploi du temps des " + self.groupeName)
        embed.description = "Du Lundi " + str(self.semaine[0]["date"].day) + " "+mois[self.semaine[0]["date"].month]+ " au Vendredi " + str(self.semaine[4]["date"].day)+ " "+mois[self.semaine[4]["date"].month]

        for jourjour in self.semaine:

            msg = ""
            for event in sorted_events:
                if self.semaine[jourjour]["date"].day == event.begin.date().day:
                    tmp = event.description.split("\n", 4)[3].split(" ")
                    professeur = ""
                    for i in range(len(tmp)-1):
                        professeur += tmp[i] + " "
                    cours_list = event.name.split(" ")
                    cours = ""
                    if len(cours_list) > 2:
                        del cours_list[0]
                        del cours_list[-1]
                    for caractere in cours_list:
                        cours += caractere + " "
                    heureDeb = event.begin.strftime('%H:%M').split(":")
                    heureFin = event.end.strftime('%H:%M').split(":")
                    vraiheureDeb = int(heureDeb[0]) + self.heureDecalage
                    vraiheureFin = int(heureFin[0]) + self.heureDecalage
                    if vraiheureDeb >= 10:
                        heureDeb = "" + str(vraiheureDeb) + ":" + heureDeb[1]
                        heureFin = str(vraiheureFin) + ":"+ heureFin[1]
                    else:
                        heureDeb = "0" + str(vraiheureDeb) + ":" + heureDeb[1]
                        heureFin = str(vraiheureFin) + ":"+ heureFin[1]
                    msg += "**" + heureDeb + "** -> **"+heureFin+"**: `" + cours + "` " + event.location + " *" + professeur + "*\n"
            
            if msg == "":
                msg = "PAS DE COURS"
            embed.add_field(name=self.semaine[jourjour]["trad"], value=msg, inline=False)
        embed.set_footer(text="Bot crée par Manolo", icon_url=self.avatar_bor)
        await interaction.response.edit_message(embed=embed)