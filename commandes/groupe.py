import discord
from discord import app_commands

from models.bdd import BDD
import services.generic as generic_service
bdd = BDD()
groupes = bdd.obtenir_tous_groupes()

choices_groupes = [discord.app_commands.Choice(name=f"{groupe.nom}", value=groupe.id) for groupe in groupes]

def get(bot):
    @bot.tree.command(name="edt-groupe", description="Emploi du temps d'un groupe")
    @app_commands.describe(groupe="Quel groupe ?")
    @app_commands.choices(groupe=choices_groupes)
    async def edt_groupe(interaction: discord.Interaction, groupe: discord.app_commands.Choice[str]):
        await interaction.response.defer()
        res = generic_service.nouveau_commande_edt_groupe(bot, groupe.value)
        if res['file']:
            await interaction.followup.send(embed=res['embed'], file=res['file'])
        else:
            await interaction.followup.send(embed=res['embed'])
