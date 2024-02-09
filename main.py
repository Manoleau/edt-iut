import discord
from discord.ext import commands
from discord import app_commands
from ics import Calendar
import requests
import datetime
import sqlite3
import re
from Button.SemaineSuivPre import BtnSemaineSuivante
from MenuSelect.ChoixJourSalleLibre import JourView


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
##conn = sqlite3.connect('Data Base/edtdiscord.db')
##cursor = conn.cursor()
#cursor.execute("SELECT * FROM edit_embed")
#print(cursor.fetchall())


@bot.event
async def on_ready():
    print('Le Bot ' + bot.user.display_name + ' Est Prêt !')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


heureDecalage = 1

data_groupe = {
    # "G1S1A": "12096",
    # "G1S1B": "12102",
    # "G2S1A": "12403",
    # "G2S1B": "12406",
    # "G3S1A": "12419",
    # "G3S1B": "12425",
    # "G4S1A": "12424",
    # "G4S1B": "12444",
    # "G5S1A": "12460",
    # "G5S1B": "12461",

    # "G1S2A": "51542",
    # "G1S2B": "51543",
    # "G2S2A": "51545",
    # "G2S2B": "51546",
    # "G3S2A": "51548",
    # "G3S2B": "51549",
    # "G4S2A": "51551",
    # "G4S2B": "51552",

    # "G1S3A": "35708",
    # "G1S3B": "35709",
    # "G2S3A": "35710",
    # "G2S3B": "35713",
    # "G4S3A": "35717",
    # "G4S3B": "35718",
    "G3S3S4": "35714",

    "G1S4A": "85875",
    "G1S4B": "85876",
    "G2S4A": "85873",
    "G2S4B": "85874",
    "G4S4A": "85877",
    "G4S4B": "85878",

    # "BUT3AGED": "6048",
    # "BUT3DACS": "6136",

    # "BUT3RA1A": "6161",
    # "BUT3RA1B": "6163",

    # "BUT3RA2A": "6165",
    # "BUT3RA2B": "6168",
}

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

jour = {
    0: {
        "trad": "Lundi"
    },
    1: {
        "trad": "Mardi"
    },
    2: {
        "trad": "Mercredi"
    },
    3: {
        "trad": "Jeudi"
    },
    4: {
        "trad": "Vendredi"
    }
}

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

option = [discord.app_commands.Choice(name=classe, value=classe) for classe in data_groupe]

@bot.tree.command(name="edt", description="Affiche un emploi du temps choisi")
@app_commands.describe(classe="Quelle classe ?")
@app_commands.choices(classe=option)
async def edt(interaction: discord.Interaction, classe: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    classeAll = classe.value
    if classeAll not in data_groupe:
        await interaction.followup.send("Veillez saisir une classe qui existe.")
    else:
        aujourdhui = datetime.date.today()
        lundi = aujourdhui - datetime.timedelta(days=aujourdhui.weekday())
        mardi = aujourdhui + datetime.timedelta(days=1 - aujourdhui.weekday() % 7)
        mercredi = aujourdhui + datetime.timedelta(days=2 - aujourdhui.weekday() % 7)
        jeudi = aujourdhui + datetime.timedelta(days=3 - aujourdhui.weekday() % 7)
        vendredi = aujourdhui + datetime.timedelta(days=4 - aujourdhui.weekday() % 7)

        if aujourdhui.weekday() == 5 or aujourdhui.weekday() == 6:
            lundi = lundi + datetime.timedelta(days=7)
            mardi = mardi + datetime.timedelta(days=7)
            mercredi = mercredi + datetime.timedelta(days=7)
            jeudi = jeudi + datetime.timedelta(days=7)
            vendredi = vendredi + datetime.timedelta(days=7)
        jour[0]["date"] = lundi
        jour[1]["date"] = mardi
        jour[2]["date"] = mercredi
        jour[3]["date"] = jeudi
        jour[4]["date"] = vendredi
        # Parse the URL
        url = 'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=' + data_groupe[
            classeAll] + '&projectId=3&calType=ical&firstDate=' + str(lundi.year) + '-' + str(lundi.month) + '-' + str(
            lundi.day) + '&lastDate=' + str(vendredi.year) + '-' + str(vendredi.month) + '-' + str(vendredi.day)

        try:
            cal = Calendar(requests.get(url).text)
        except Exception as e:
            print(e)
            await interaction.followup.send("Erreur : veuillez réessayer.")
        embed = discord.Embed()
        # Print all the event
        events = cal.events
        sorted_events = sorted(events, reverse=False)
        embed.set_author(name="Emploi du temps des " + classeAll)
        embed.description = "Du Lundi " + str(lundi.day) + " "+mois[lundi.month]+" au Vendredi " + str(vendredi.day) + " "+mois[vendredi.month]

        for jourjour in jour:

            msg = ""
            for event in sorted_events:
                if jour[jourjour]["date"].day == event.begin.date().day:
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
                    vraiheureDeb = int(heureDeb[0]) + heureDecalage
                    vraiheureFin = int(heureFin[0]) + heureDecalage
                    if vraiheureDeb >= 10:
                        heureDeb = "" + str(vraiheureDeb) + ":" + heureDeb[1]
                        heureFin = str(vraiheureFin) + ":"+ heureFin[1]
                    else:
                        heureDeb = "0" + str(vraiheureDeb) + ":" + heureDeb[1]
                        heureFin = str(vraiheureFin) + ":"+ heureFin[1]
                    msg += "**" + heureDeb + "** -> **"+heureFin+"**: `" + cours + "` " + event.location + " *" + professeur + "*\n"
            if msg == "":
                msg = "PAS DE COURS"
            embed.add_field(name=jour[jourjour]["trad"], value=msg, inline=False)
        embed.set_footer(text="Bot crée par Manolo", icon_url=bot.user.display_avatar.url)
        await interaction.followup.send(embed=embed, view=BtnSemaineSuivante(jour, data_groupe[classeAll], classeAll, heureDecalage, bot.user.display_avatar.url))


@bot.tree.command(name="edt-salle", description="Affiche un emploi du temps d'une salle choisie")
@app_commands.describe(salle="Quelle salle ?")
@app_commands.choices(
    salle=[discord.app_commands.Choice(name=salle + " (" + data_salle[salle]["type"] + ")", value=salle) for salle in
           data_salle])
async def edtsalle(interaction: discord.Interaction, salle: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    salle = salle.value
    if salle not in data_salle:
        await interaction.followup.send("Veillez saisir une salle qui existe.")
    else:
        aujourdhui = datetime.date.today()
        lundi = aujourdhui - datetime.timedelta(days=aujourdhui.weekday())
        mardi = aujourdhui + datetime.timedelta(days=1 - aujourdhui.weekday() % 7)
        mercredi = aujourdhui + datetime.timedelta(days=2 - aujourdhui.weekday() % 7)
        jeudi = aujourdhui + datetime.timedelta(days=3 - aujourdhui.weekday() % 7)
        vendredi = aujourdhui + datetime.timedelta(days=4 - aujourdhui.weekday() % 7)

        if aujourdhui.weekday() == 5 or aujourdhui.weekday() == 6:
            lundi = lundi + datetime.timedelta(days=7)
            mardi = mardi + datetime.timedelta(days=7)
            mercredi = mercredi + datetime.timedelta(days=7)
            jeudi = jeudi + datetime.timedelta(days=7)
            vendredi = vendredi + datetime.timedelta(days=7)
        jour[0]["date"] = lundi
        jour[1]["date"] = mardi
        jour[2]["date"] = mercredi
        jour[3]["date"] = jeudi
        jour[4]["date"] = vendredi
        # Parse the URL
        url = 'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=' + \
              data_salle[salle]["id"] + '&projectId=3&calType=ical&firstDate=' + str(lundi.year) + '-' + str(
            lundi.month) + '-' + str(lundi.day) + '&lastDate=' + str(vendredi.year) + '-' + str(
            vendredi.month) + '-' + str(vendredi.day)
        try:
            cal = Calendar(requests.get(url).text)
        except Exception as e:
            print(e)
            await interaction.followup.send("Erreur : veuillez réessayer.")
        embed = discord.Embed()

        events = cal.events
        sorted_events = sorted(events, reverse=False)
        embed.set_author(name="Emploi du temps de la salle " + salle)
        embed.description = "Du lundi " + str(lundi.day) + " au vendredi " + str(vendredi.day)

        for jourjour in jour:
            msg = ""
            for event in sorted_events:

                if jour[jourjour]["date"].day == event.begin.date().day:
                    professeur = event.description.split("\n", 4)[3]
                    heure = event.begin.strftime('%H:%M').split(":")
                    vraiheure = int(heure[0]) + heureDecalage
                    if vraiheure >= 10:
                        heure = "" + str(vraiheure) + ":" + heure[1]
                    else:
                        heure = "0" + str(vraiheure) + ":" + heure[1]
                    msg += "**" + heure + "**: `" + event.name + "` *" + professeur + "*\n"
            if msg == "":
                msg = "PAS DE COURS"
            embed.add_field(name=jour[jourjour]["trad"], value=msg, inline=False)
        embed.set_footer(text="Bot crée par Manolo", icon_url=bot.user.display_avatar.url)
        await interaction.followup.send(embed=embed)


@bot.tree.command(name="salle-libre", description="Affiche toutes les salle libres")
@app_commands.describe(type="Quel type de salle ?")
@app_commands.choices(type=[
    discord.app_commands.Choice(name="Info", value="info"),
    discord.app_commands.Choice(name="TD", value="TD"),
    discord.app_commands.Choice(name="Réseau", value="reseau"),
    discord.app_commands.Choice(name="Autre", value="autre")
])
async def sallelibre(interaction: discord.Interaction, type: discord.app_commands.Choice[str]):
    await interaction.response.defer()
    
    type = type.value
    
    aujourdhui = datetime.date.today()
    liste_jour = [{
        "name": jour[aujourdhui.weekday()]["trad"] + " "+str(aujourdhui.day)+ " "+mois[aujourdhui.month] + " " +str(aujourdhui.year),
        "date": 0
    }]
    j = 0
    for i in range(24):
        tmpjour = aujourdhui + datetime.timedelta(days=j+1)
        while tmpjour.weekday() == 5 or tmpjour.weekday() == 6:
            tmpjour = tmpjour + datetime.timedelta(days=1)
            j += 1
        liste_jour.append({
            "name": jour[tmpjour.weekday()]["trad"] + " "+str(tmpjour.day)+ " "+mois[tmpjour.month] + " " +str(tmpjour.year),
            "date": j+1
        })
        j += 1
    await interaction.followup.send(view=JourView(liste_jour, type, bot.user.display_avatar.url))
    # aujourdhui = datetime.date.today()

    # liste_salle = []
    # liste_info_salle = []
    # if interaction.guild is not None:
    #     await interaction.channel.send("Chargement...")
    #     lastmessage = interaction.channel.last_message
    # for salle in data_salle:
    #     if data_salle[salle]["type"] == type:
    #         liste_salle.append({
    #             salle: data_salle[salle]
    #         })

    #         url = 'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=' + \
    #               data_salle[salle]["id"] + '&projectId=3&calType=ical&firstDate=' + str(aujourdhui.year) + '-' + str(
    #             aujourdhui.month) + '-' + str(aujourdhui.day) + '&lastDate=' + str(aujourdhui.year) + '-' + str(
    #             aujourdhui.month) + '-' + str(aujourdhui.day)
    #         try:
    #             cal = Calendar(requests.get(url).text)
    #         except Exception as e:
    #             print(e)
    #             await interaction.followup.send("Erreur : veuillez réessayer.")
    #         events = cal.events
    #         sorted_events = sorted(events, reverse=False)
    #         liste_info_salle.append(sorted_events)
    #         if interaction.guild is not None:
    #             await lastmessage.edit(content="Salle " + salle + " :white_check_mark:")
    # heureDebut = datetime.datetime(year=aujourdhui.year, month=aujourdhui.month, day=aujourdhui.day, hour=8, minute=0)
    # heureFin = datetime.datetime(year=aujourdhui.year, month=aujourdhui.month, day=aujourdhui.day, hour=18, minute=0)
    # salleLibreHeure = {}
    # for salle in liste_info_salle:
    #     ""
    #     if len(salle) > 1:

    #         previousEnd = heureDebut
    #         for i in range(len(salle)):
    #             start = salle[i].begin.datetime
    #             vraistart = datetime.datetime(year=start.year, month=start.month, day=start.day,
    #                                           hour=start.hour + heureDecalage, minute=start.minute)
    #             gap = vraistart - previousEnd
    #             if gap.total_seconds() > 0:
    #                 previousEndHeure = previousEnd.strftime('%H:%M').split(":")
    #                 vraiHeureStart = vraistart.strftime('%H:%M').split(":")
    #                 previousEndHeure = "" + previousEndHeure[0] + ":" + previousEndHeure[1]
    #                 vraiHeureStart = "" + str(vraiHeureStart[0]) + ":" + vraiHeureStart[1]

    #                 tmpHeureDecal = previousEndHeure + " --> " + vraiHeureStart
    #                 if tmpHeureDecal not in salleLibreHeure:
    #                     salleLibreHeure[tmpHeureDecal] = []
    #                 salleLibreHeure[tmpHeureDecal].append(salle[i].location)
    #             fin = salle[i].end.datetime
    #             previousEnd = datetime.datetime(year=fin.year, month=fin.month, day=fin.day,
    #                                             hour=fin.hour + heureDecalage, minute=fin.minute)
    #         if previousEnd < heureFin:

    #             previousEndHeure = previousEnd.strftime('%H:%M').split(":")
    #             previousEndHeure = "" + str(previousEndHeure[0]) + ":" + previousEndHeure[1]
    #             vraiHeureFin = heureFin.strftime('%H:%M').split(":")
    #             vraiHeureFin = "" + str(vraiHeureFin[0]) + ":" + vraiHeureFin[1]

    #             tmpHeureDecal = previousEndHeure + " --> " + vraiHeureFin
    #             if tmpHeureDecal not in salleLibreHeure:
    #                 salleLibreHeure[tmpHeureDecal] = []
    #             salleLibreHeure[tmpHeureDecal].append(salle[i].location)
    # embed = discord.Embed()
    # embed.set_author(name="Heure de disponibilité des salles " + type)
    # for heure in salleLibreHeure:
    #     msg = ""
    #     for salle in salleLibreHeure[heure]:
    #         msg += salle + "\n"
    #     embed.add_field(name=heure, value=msg, inline=False)
    # if interaction.guild is not None:
    #     await lastmessage.delete()
    # embed.set_footer(text="Bot crée par Manolo", icon_url=bot.user.display_avatar.url)
    # await interaction.followup.send(embed=embed)

#@bot.tree.command(name="test", description="Affiche toutes les salle libres")
#async def test(interaction: discord.Interaction, test2: discord.User):
#    await interaction.response.defer()
#    print(test2)
#    await interaction.followup.send("test")

@bot.event
async def on_message(message:discord.Message):
    if message.author.id == 1205572414797381722 and message.content == "Loic ratio":  # Ignorer les messages provenant des bots
        loicid = 422208112225812511
        loic = bot.get_guild(800411029682257930).get_member(loicid)
        if loic.voice:
            await loic.move_to(None)
        await message.delete()

bot.run("TOKEN")