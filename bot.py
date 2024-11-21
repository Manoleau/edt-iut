import discord
from discord.ext import commands
import commandes.edt_salle as edt_salle
import commandes.edt_groupe as edt_groupe
# import commandes.rappel as rappel
import commandes.ajout_groupe as ajout_groupe
import commandes.supprimer_groupe as supprimer_groupe
import commandes.liste_groupes as groupes
import logging
logger = logging.getLogger(__name__)
class EdtIUTBot(commands.Bot):
    def __init__(self)-> None:
        super().__init__(command_prefix="!", intents=discord.Intents.all())
        self.commandes = None
    async def setup_hook(self) -> None:
        try:
            self.tree.clear_commands(guild=None)
            edt_salle.get(self)
            edt_groupe.get(self)
            # rappel.get(self)
            ajout_groupe.get(self)
            supprimer_groupe.get(self)
            groupes.get(self)
            self.commandes = await self.tree.sync()
        except Exception as e:
            print(e)

    async def on_ready(self) -> None:

        print('Le Bot ' + self.user.display_name + ' Est Prêt !')
        print(f"Synced {len(self.commandes)} command(s)")

#
# @bot.tree.command(name="salle-libre", description="Affiche toutes les salle libres")
# @app_commands.describe(type="Quel type de salle ?")
# @app_commands.choices(type=[
#     discord.app_commands.Choice(name="Info", value="info"),
#     discord.app_commands.Choice(name="TD", value="TD"),
#     discord.app_commands.Choice(name="Réseau", value="reseau"),
#     discord.app_commands.Choice(name="Autre", value="autre")
# ])
# async def sallelibre(interaction: discord.Interaction, type: discord.app_commands.Choice[str]):
#     await interaction.response.defer()
#
#     type = type.value
#
#     aujourdhui = datetime.date.today()
#     liste_jour = [{
#         "name": jour[aujourdhui.weekday()]["trad"] + " " + str(aujourdhui.day) + " " + mois[
#             aujourdhui.month] + " " + str(aujourdhui.year),
#         "date": 0
#     }]
#     j = 0
#     for i in range(24):
#         tmpjour = aujourdhui + datetime.timedelta(days=j + 1)
#         while tmpjour.weekday() == 5 or tmpjour.weekday() == 6:
#             tmpjour = tmpjour + datetime.timedelta(days=1)
#             j += 1
#         liste_jour.append({
#             "name": jour[tmpjour.weekday()]["trad"] + " " + str(tmpjour.day) + " " + mois[tmpjour.month] + " " + str(
#                 tmpjour.year),
#             "date": j + 1
#         })
#         j += 1
#     await interaction.followup.send(view=JourView(liste_jour, type, bot.user.display_avatar.url))
#     # aujourdhui = datetime.date.today()
#
#     # liste_salle = []
#     # liste_info_salle = []
#     # if interaction.guild is not None:
#     #     await interaction.channel.send("Chargement...")
#     #     lastmessage = interaction.channel.last_message
#     # for salle in data_salle:
#     #     if data_salle[salle]["type"] == type:
#     #         liste_salle.append({
#     #             salle: data_salle[salle]
#     #         })
#
#     #         url = 'https://adelb.univ-lyon1.fr/jsp/custom/modules/plannings/anonymous_cal.jsp?resources=' + \
#     #               data_salle[salle]["id"] + '&projectId=3&calType=ical&firstDate=' + str(aujourdhui.year) + '-' + str(
#     #             aujourdhui.month) + '-' + str(aujourdhui.day) + '&lastDate=' + str(aujourdhui.year) + '-' + str(
#     #             aujourdhui.month) + '-' + str(aujourdhui.day)
#     #         try:
#     #             cal = Calendar(requests.get(url).text)
#     #         except Exception as e:
#     #             print(e)
#     #             await interaction.followup.send("Erreur : veuillez réessayer.")
#     #         events = cal.events
#     #         sorted_events = sorted(events, reverse=False)
#     #         liste_info_salle.append(sorted_events)
#     #         if interaction.guild is not None:
#     #             await lastmessage.edit(content="Salle " + salle + " :white_check_mark:")
#     # heureDebut = datetime.datetime(year=aujourdhui.year, month=aujourdhui.month, day=aujourdhui.day, hour=8, minute=0)
#     # heureFin = datetime.datetime(year=aujourdhui.year, month=aujourdhui.month, day=aujourdhui.day, hour=18, minute=0)
#     # salleLibreHeure = {}
#     # for salle in liste_info_salle:
#     #     ""
#     #     if len(salle) > 1:
#
#     #         previousEnd = heureDebut
#     #         for i in range(len(salle)):
#     #             start = salle[i].begin.datetime
#     #             vraistart = datetime.datetime(year=start.year, month=start.month, day=start.day,
#     #                                           hour=start.hour + heureDecalage, minute=start.minute)
#     #             gap = vraistart - previousEnd
#     #             if gap.total_seconds() > 0:
#     #                 previousEndHeure = previousEnd.strftime('%H:%M').split(":")
#     #                 vraiHeureStart = vraistart.strftime('%H:%M').split(":")
#     #                 previousEndHeure = "" + previousEndHeure[0] + ":" + previousEndHeure[1]
#     #                 vraiHeureStart = "" + str(vraiHeureStart[0]) + ":" + vraiHeureStart[1]
#
#     #                 tmpHeureDecal = previousEndHeure + " --> " + vraiHeureStart
#     #                 if tmpHeureDecal not in salleLibreHeure:
#     #                     salleLibreHeure[tmpHeureDecal] = []
#     #                 salleLibreHeure[tmpHeureDecal].append(salle[i].location)
#     #             fin = salle[i].end.datetime
#     #             previousEnd = datetime.datetime(year=fin.year, month=fin.month, day=fin.day,
#     #                                             hour=fin.hour + heureDecalage, minute=fin.minute)
#     #         if previousEnd < heureFin:
#
#     #             previousEndHeure = previousEnd.strftime('%H:%M').split(":")
#     #             previousEndHeure = "" + str(previousEndHeure[0]) + ":" + previousEndHeure[1]
#     #             vraiHeureFin = heureFin.strftime('%H:%M').split(":")
#     #             vraiHeureFin = "" + str(vraiHeureFin[0]) + ":" + vraiHeureFin[1]
#
#     #             tmpHeureDecal = previousEndHeure + " --> " + vraiHeureFin
#     #             if tmpHeureDecal not in salleLibreHeure:
#     #                 salleLibreHeure[tmpHeureDecal] = []
#     #             salleLibreHeure[tmpHeureDecal].append(salle[i].location)
#     # embed = discord.Embed()
#     # embed.set_author(name="Heure de disponibilité des salles " + type)
#     # for heure in salleLibreHeure:
#     #     msg = ""
#     #     for salle in salleLibreHeure[heure]:
#     #         msg += salle + "\n"
#     #     embed.add_field(name=heure, value=msg, inline=False)
#     # if interaction.guild is not None:
#     #     await lastmessage.delete()
#     # embed.set_footer(text="Bot crée par Manolo", icon_url=bot.user.display_avatar.url)
#     # await interaction.followup.send(embed=embed)