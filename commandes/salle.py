import discord
from discord import app_commands

from models.bdd import BDD
import services.generic as generic_service
bdd = BDD()
salles = bdd.obtenir_toutes_salles()

choices_salles = [discord.app_commands.Choice(name=f"{salle.nom} ({salle.type.value})", value=salle.id) for salle in salles]

def get(bot):
    @bot.tree.command(name="edt-salle", description="Emploi du temps d'une salle")
    @app_commands.describe(salle="Quelle salle ?")
    @app_commands.choices(salle=choices_salles)
    async def edt_salle(interaction: discord.Interaction, salle: discord.app_commands.Choice[str]):
        await interaction.response.defer()
        res = generic_service.nouveau_commande_edt_salle(bot, salle.value)
        if res['file']:
            await interaction.followup.send(embed=res['embed'], file=res['file'])
        else:
            await interaction.followup.send(embed=res['embed'])
