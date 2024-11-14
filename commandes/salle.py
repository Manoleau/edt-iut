
import discord
from discord import app_commands
from models.bdd import BDD
import services.embed as embed_service
import services.date as date_service
import services.calendar as calendar_service
bdd = BDD()

salles = bdd.obtenir_toutes_salles()

choices_salles = [discord.app_commands.Choice(name=f"{salle.nom} ({salle.type.value})", value=salle.id) for salle in salles]

def get(bot):
    @bot.tree.command(name="edt-salle", description="Emploi du temps d'une salle")
    @app_commands.describe(salle="Quelle salle ?")
    @app_commands.choices(salle=choices_salles)
    async def edt_salle(interaction: discord.Interaction, salle: discord.app_commands.Choice[str]):
        await interaction.response.defer()
        salle = bdd.obtenir_salle_avec_id(salle.value)
        if salle:
            jours = date_service.obtenir_jour_semaine_actuel()
            events = calendar_service.obtenir(salle.id, jours[0], jours[4])
            event = events[1]
            # for event in events:
            print(f"nom : {event.name}")
            print(f"description : {event.description}")
            print(f"duration : {event.duration}")
            embed = embed_service.obtenir_embed(
                title=f"Salle {salle.nom}"
            )
            # embed.add_field(name="GGEZ", value="GGEZ")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send("Veillez saisir une classe qui existe.")

