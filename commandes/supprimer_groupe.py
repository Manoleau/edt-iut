import json

import discord
from discord import app_commands
import services.embed as embed_service
from models.bdd import BDD
bdd = BDD()

def get(bot):
    @bot.tree.command(name="supprimer-groupe", description="Supprime un groupe de la base de données.")
    @app_commands.describe(groupe="Nom du groupe.")
    async def supprimer_groupe(interaction: discord.Interaction, groupe:str):
        await interaction.response.defer()
        if interaction.user.id == 334695006663344151:
            bdd.connect()
            if bdd._delete('groupe', ['id'], (groupe,)):
                bdd.disconnect()
                with open('data.json', "r", encoding="utf-8") as file:
                    data = json.load(file)
                data["groupe"] = [data_groupe for data_groupe in data["groupe"] if data_groupe["id"] != groupe]
                with open('data.json', "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                await interaction.followup.send(embed=embed_service.obtenir_succes(f"Le groupe a été supprimé avec succés.", bot.user.display_avatar.url))
            else:
                bdd.disconnect()
                await interaction.followup.send(embed=embed_service.obtenir_erreur(f"Impossible d'ajouter de supprimer ce groupe car il n'existe pas.", bot.user.display_avatar.url))

        else:
            await interaction.followup.send(embed=embed_service.obtenir_erreur("Vous n'avez pas les droits.", bot.user.display_avatar.url))

    @supprimer_groupe.autocomplete("groupe")
    async def groupe_autocomplete(
            interaction: discord.Interaction,
            current: str
    ) -> list[app_commands.Choice[str]]:
        groupes = bdd.obtenir_tous_groupes()
        data = []
        i = 0
        current = current.lower()
        while len(data) < 25 and i < len(groupes):
            groupe = groupes[i]
            if current in groupe.nom.lower() or current in groupe.id.lower():
                data.append(app_commands.Choice(name=f"{groupe.nom}", value=groupe.id))
            i += 1
        return data