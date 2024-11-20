import discord
import services.embed as embed_service
from models.bdd import BDD
bdd = BDD()

def get(bot):
    @bot.tree.command(name="groupes", description="Liste des groupes")
    async def groupes(interaction: discord.Interaction):
        await interaction.response.defer()
        groupes = bdd.obtenir_tous_groupes()
        message = ">>> "
        for groupe in groupes:
            message += f"Groupe {groupe.nom} => id = {groupe.id}\n"
        await interaction.followup.send(embed=embed_service.obtenir_succes(message, bot.user.display_avatar.url))