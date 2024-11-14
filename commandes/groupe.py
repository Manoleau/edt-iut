import discord
import datetime
from discord import app_commands

from models.bdd import BDD
import services.embed as embed_service
import services.date as date_service
import services.calendar as calendar_service
import services.media as media_service
from models.jour import Jour
bdd = BDD()
groupes = bdd.obtenir_tous_groupes()

choices_groupes = [discord.app_commands.Choice(name=f"{groupe.nom}", value=groupe.id) for groupe in groupes]

def get(bot):
    @bot.tree.command(name="edt-groupe", description="Emploi du temps d'un groupe")
    @app_commands.describe(groupe="Quel groupe ?")
    @app_commands.choices(groupe=choices_groupes)
    async def edt_groupe(interaction: discord.Interaction, groupe: discord.app_commands.Choice[str]):
        await interaction.response.defer()
        groupe = bdd.obtenir_groupe_avec_id(groupe.value)
        if groupe:
            jours = date_service.obtenir_jour_semaine_actuel()
            premier_jour = jours[0]
            dernier_jour = jours[4]
            cal = calendar_service.obtenir(groupe.id, premier_jour, dernier_jour)
            heure_decalage = date_service.obtenir_heure_decalage()
            horaires = []
            check_horaires = []
            indices_horaires = {}
            for event in cal['events']:
                event.begin += datetime.timedelta(hours=heure_decalage)
                event.end += datetime.timedelta(hours=heure_decalage)
                horaire = f"{event.begin.strftime('%H:%M')} - {event.end.strftime('%H:%M')}"
                if horaire not in check_horaires:
                    horaires.append({
                        'time': horaire,
                        'cours': []
                    })
                    check_horaires.append(horaire)
            horaires_tries = sorted(horaires, key=lambda x: datetime.datetime.strptime(x['time'].split(' - ')[0], '%H:%M'))
            for i in range(len(horaires_tries)):
                indices_horaires[horaires_tries[i]['time']] = {
                    'indice': i
                }
            for jour in jours:
                for event in cal['events']:
                    if jour.day == event.begin.date().day:
                        horaire = f"{event.begin.strftime('%H:%M')} - {event.end.strftime('%H:%M')}"
                        for i in range(jour.weekday() - len(horaires_tries[indices_horaires[horaire]['indice']]['cours'])):
                            horaires_tries[indices_horaires[horaire]['indice']]['cours'].append('-')
                        description = [item for item in event.description.split("\n") if item]
                        try:
                            int(description[0])
                            horaires_tries[indices_horaires[horaire]['indice']]['cours'].append(f'{event.name}')
                        except ValueError:
                            prof = description[1]
                            horaires_tries[indices_horaires[horaire]['indice']]['cours'].append(f'{event.name}<br>{prof}')
            for horaire in horaires_tries:
                while len(horaire['cours']) < 5:
                    horaire['cours'].append('-')
            data = {
                'jours' : [Jour(i) for i in range(len(jours))],
                'heures' : horaires_tries,
            }
            nom_fichier = f'{groupe.nom.lower()}_{premier_jour.strftime('%Y-%m-%d')}_{dernier_jour.strftime('%Y-%m-%d')}'
            media_service.create_html_edt(nom_fichier, data)
            image = media_service.create_image_edt(nom_fichier)
            res = embed_service.obtenir_edt_groupe(groupe, premier_jour, dernier_jour, image, bot.user.display_avatar.url, cal['ics'])
            await interaction.followup.send(embed=res['embed'], file=res['file'])
        else:
            await interaction.followup.send("Veillez saisir une classe qui existe.")

