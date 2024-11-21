import json

import discord
from discord import app_commands
import services.embed as embed_service
import services.calendar as calendar_service
import services.date as date_service
from models.bdd import BDD
bdd = BDD()

def get(bot):
    @bot.tree.command(name="ajout-groupe", description="Ajoute un groupe à la base de données")
    @app_commands.describe(id="Id du groupe.")
    @app_commands.describe(nom="Nom du groupe.")
    async def ajout_groupe(interaction: discord.Interaction, id: str, nom:str):
        await interaction.response.defer()
        if interaction.user.id == 334695006663344151:
            jours = date_service.obtenir_jour_semaine_actuel()

            test = calendar_service.obtenir(id, jours[0], jours[4])
            if test['ics'] is not None:
                if bdd._insert_one('groupe', ['id', 'nom'], (id, nom)):
                    with open('data.json', "r", encoding="utf-8") as file:
                        data = json.load(file)
                    data["groupe"].append({'id' : id, 'nom' : nom})
                    with open(data.json, "w", encoding="utf-8") as file:
                        json.dump(data, file, indent=4, ensure_ascii=False)
                    await interaction.followup.send(embed=embed_service.obtenir_succes(f"Le groupe {nom} a été ajouté avec succés.", bot.user.display_avatar.url))
                else:
                    await interaction.followup.send(embed=embed_service.obtenir_erreur(f"Impossible d'ajouter le groupe {nom} ({id}) car il existe déjà.", bot.user.display_avatar.url))
            else:
                await interaction.followup.send(embed=embed_service.obtenir_erreur(f"Aucun emploi du temps existe sous l'id {id}.", bot.user.display_avatar.url))

        else:
            await interaction.followup.send(embed=embed_service.obtenir_erreur("Vous n'avez pas les droits.", bot.user.display_avatar.url))
