import datetime

import discord
from discord import app_commands

from models.bdd import BDD
import services.generic as generic_service
bdd = BDD()

def get(bot):
    @bot.tree.command(name="edt-groupe", description="Emploi du temps d'un groupe")
    @app_commands.describe(groupe="Quel groupe ?")
    async def edt_groupe(interaction: discord.Interaction, groupe: str, update:bool = False):
        await interaction.response.defer()
        res = generic_service.nouveau_commande_edt_groupe(bot, groupe, update=update)
        if res['file']:
            await interaction.followup.send(embed=res['embed'], file=res['file'], view=res['view'])
        else:
            await interaction.followup.send(embed=res['embed'])

    @edt_groupe.autocomplete("groupe")
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