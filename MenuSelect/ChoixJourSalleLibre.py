
from typing import Any
import discord
from discord.ui import View, Select
import datetime
from ics import Calendar
import requests
heureDecalage = 1
data_salle = {
    "S04": {
        "type": "autre",
        "id": "9113",
    },
    "S18": {
        "type": "reseau",
        "id": "126",
    },
    "S21": {
        "type": "autre",
        "id": "134",
    },
    "S23": {
        "type": "reseau",
        "id": "132",
    },

    "S01": {
        "type": "info",
        "id": "118",
    },
    "S03": {
        "type": "info",
        "id": "119",
    },
    "S13": {
        "type": "info",
        "id": "120",
    },
    "S14": {
        "type": "info",
        "id": "121",
    },
    "S16": {
        "type": "info",
        "id": "122",
    },
    "S17": {
        "type": "info",
        "id": "123",
    },
    "S22": {
        "type": "info",
        "id": "135",
    },
    "S24": {
        "type": "info",
        "id": "136",
    },
    "S26": {
        "type": "info",
        "id": "133",
    },
    "S27": {
        "type": "info",
        "id": "9188",
    },

    "040": {
        "type": "TD",
        "id": "344",
    },
    "S10": {
        "type": "TD",
        "id": "127",
    },
    "S11": {
        "type": "TD",
        "id": "128",
    },
    "S12": {
        "type": "TD",
        "id": "129",
    },
    "S15": {
        "type": "TD",
        "id": "130",
    },
    "S25": {
        "type": "TD",
        "id": "131",
    }
}
class JourSelect(Select):
    def __init__(self, viewMenu, liste_jour:list, type:str, avatar_url:str) -> None:
        super().__init__(placeholder="Choisissez un jour", options=[discord.SelectOption(label=jour["name"], value=jour["date"]) for jour in liste_jour])
        self.viewMenu = viewMenu
        self.typeSalle = type
        self.jourselect = None
        self.liste_jour = liste_jour
        self.avatar_url =  avatar_url
        self.message = None

    async def callback(self, interaction: discord.Interaction) -> Any:
        if self.message is not None:
            await self.message.delete()
        await interaction.response.edit_message(view=self.view)
        try:
            aujourdhui = datetime.date.today()
            self.jourselect = aujourdhui + datetime.timedelta(days=int(self.values[0]))

            liste_salle = []
            liste_info_salle = []
            if interaction.guild is not None:
                await interaction.channel.send("Chargement...")
                lastmessage = interaction.channel.last_message
            for salle in data_salle:
                if data_salle[salle]["type"] == self.typeSalle:
                    liste_salle.append({
                        salle: data_salle[salle]
                    })

                    url = 'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=' + \
                        data_salle[salle]["id"] + '&projectId=3&calType=ical&firstDate=' + str(self.jourselect.year) + '-' + str(
                        self.jourselect.month) + '-' + str(self.jourselect.day) + '&lastDate=' + str(self.jourselect.year) + '-' + str(
                        self.jourselect.month) + '-' + str(self.jourselect.day)
                    try:
                        cal = Calendar(requests.get(url).text)
                    except Exception as e:
                        print(e)
                        await interaction.followup.send("Erreur : veuillez réessayer.")
                    events = cal.events
                    sorted_events = sorted(events, reverse=False)
                    liste_info_salle.append(sorted_events)
                    if interaction.guild is not None:
                        await lastmessage.edit(content="Salle " + salle + " :white_check_mark:")
            heureDebut = datetime.datetime(year=self.jourselect.year, month=self.jourselect.month, day=self.jourselect.day, hour=8, minute=0)
            heureFin = datetime.datetime(year=self.jourselect.year, month=self.jourselect.month, day=self.jourselect.day, hour=18, minute=0)
            salleLibreHeure = {}
            for salle in liste_info_salle:
                ""
                if len(salle) > 1:

                    previousEnd = heureDebut
                    for i in range(len(salle)):
                        start = salle[i].begin.datetime
                        vraistart = datetime.datetime(year=start.year, month=start.month, day=start.day,
                                                    hour=start.hour + heureDecalage, minute=start.minute)
                        
                        gap = vraistart - previousEnd
                        if gap.total_seconds() > 0:
                            previousEndHeure = previousEnd.strftime('%H:%M').split(":")
                            vraiHeureStart = vraistart.strftime('%H:%M').split(":")
                            previousEndHeure = "" + previousEndHeure[0] + ":" + previousEndHeure[1]
                            vraiHeureStart = "" + str(vraiHeureStart[0]) + ":" + vraiHeureStart[1]

                            tmpHeureDecal = previousEndHeure + " --> " + vraiHeureStart
                            if tmpHeureDecal not in salleLibreHeure:
                                salleLibreHeure[tmpHeureDecal] = []
                            salleLibreHeure[tmpHeureDecal].append(salle[i].location)
                        fin = salle[i].end.datetime
                        if fin.hour > 18:
                            previousEnd = datetime.datetime(year=fin.year, month=fin.month, day=fin.day,
                                                        hour=18 + heureDecalage, minute=fin.minute)
                        else:
                            previousEnd = datetime.datetime(year=fin.year, month=fin.month, day=fin.day,
                                                        hour=fin.hour + heureDecalage, minute=fin.minute)
                        
                    if previousEnd < heureFin:

                        previousEndHeure = previousEnd.strftime('%H:%M').split(":")
                        previousEndHeure = "" + str(previousEndHeure[0]) + ":" + previousEndHeure[1]
                        vraiHeureFin = heureFin.strftime('%H:%M').split(":")
                        vraiHeureFin = "" + str(vraiHeureFin[0]) + ":" + vraiHeureFin[1]

                        tmpHeureDecal = previousEndHeure + " --> " + vraiHeureFin
                        if tmpHeureDecal not in salleLibreHeure:
                            salleLibreHeure[tmpHeureDecal] = []
                        salleLibreHeure[tmpHeureDecal].append(salle[i].location)
            embed = discord.Embed()
            for jour in self.liste_jour:
                if jour["date"] == int(self.values[0]):
                    nameJour = jour["name"]
            embed.set_author(name=nameJour+"\nHeure de disponibilité des salles " + self.typeSalle)
            def heure_debut(plage_horaire):
                return plage_horaire.split(' ')[0]

            salleLibreHeure_trie = dict(sorted(salleLibreHeure.items(), key=lambda item: heure_debut(item[0])))

            if len(salleLibreHeure_trie) == 0:
                embed.set_author(name=nameJour+"\nAucune salle libre")
            else:
                embed.set_author(name=nameJour+"\nHeure de disponibilité des salles " + self.typeSalle)
                for heure in salleLibreHeure_trie:
                    msg = ""
                    for salle in salleLibreHeure_trie[heure]:
                        msg += salle + "\n"
                    embed.add_field(name=heure, value=msg, inline=False)
            if interaction.guild is not None:
                await lastmessage.delete()
            embed.set_footer(text="Bot crée par Manolo", icon_url=self.avatar_url)
            self.message = await interaction.channel.send(embed=embed, content=None)
        except Exception as e:
            print(e)
            if interaction.guild is not None:
                await lastmessage.delete()
            self.message = await interaction.channel.send(embed=None, content="Une erreur s'est produite, veillez réessayer.")

class JourView(View):
    ""
    def __init__(self, liste_jour:list, type:str, avatar_url:str):
        super().__init__()
        self.add_item(JourSelect(self, liste_jour, type, avatar_url))