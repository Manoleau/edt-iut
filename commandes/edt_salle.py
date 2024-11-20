import discord
from discord import app_commands

from models.bdd import BDD
import services.generic as generic_service
bdd = BDD()
def get(bot):
    @bot.tree.command(name="edt-salle", description="Emploi du temps d'une salle")
    @app_commands.describe(salle="Quelle salle ?")
    async def edt_salle(interaction: discord.Interaction, salle: str, update:bool = False):
        await interaction.response.defer()
        res = generic_service.nouveau_commande_edt_salle(bot, salle, update=update)
        if res['file']:
            await interaction.followup.send(embed=res['embed'], file=res['file'], view=res['view'])
        else:
            await interaction.followup.send(embed=res['embed'])

    @edt_salle.autocomplete("salle")
    async def salle_autocomplete(
            interaction: discord.Interaction,
            current: str
    ) -> list[app_commands.Choice[str]]:
        salles = bdd.obtenir_toutes_salles()
        data = []
        i = 0
        current = current.lower()
        while len(data) < 25 and i < len(salles):
            salle = salles[i]
            if current in salle.nom.lower() or current in salle.type.value.lower() or current in salle.id.lower():
                data.append(app_commands.Choice(name=f"{salle.nom} ({salle.type.value})", value=salle.id))
            i += 1
        return data
