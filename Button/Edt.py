import discord
from discord.ui import View, Button
import datetime
import services.generic as generic_service
from models.groupe import Groupe
from models.salle import Salle

class ButtonsEdt(View):
    def __init__(self, bot, jour:datetime.date, model:Salle | Groupe, ics_url:str):
        super().__init__()
        self.jour = jour
        self.bot = bot
        self.model = model
        self.add_item(Button(label="ICS", style=discord.ButtonStyle.link, url=ics_url))

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def semainePreBtn(self, interaction: discord.Interaction, button: Button):
        self.jour = self.jour - datetime.timedelta(days=7)
        with_groupe = self.model.__class__.__name__ == 'Salle'
        res = generic_service.nouveau_commande_edt(self.bot, self.model, update=False, with_groupe=with_groupe, jour_semaine=self.jour)
        if res['file']:
            await interaction.channel.send(embed=res['embed'], file=res['file'], view=res['view'])
        else:
            await interaction.channel.send(embed=res['embed'])
        await interaction.message.delete()


    @discord.ui.button(label="Mettre à jour", style=discord.ButtonStyle.primary)
    async def update(self, interaction: discord.Interaction, button: Button):
        with_groupe = self.model.__class__.__name__ == 'Salle'
        res = generic_service.nouveau_commande_edt(self.bot, self.model, update=True, with_groupe=with_groupe, jour_semaine=self.jour)
        if res['file']:
            await interaction.channel.send(embed=res['embed'], file=res['file'], view=res['view'])
        else:
            await interaction.channel.send(embed=res['embed'])
        await interaction.message.delete()

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def semaineSuivBtn(self, interaction: discord.Interaction, button: Button):
        self.jour = self.jour + datetime.timedelta(days=7)
        with_groupe = self.model.__class__.__name__ == 'Salle'
        res = generic_service.nouveau_commande_edt(self.bot, self.model, update=False, with_groupe=with_groupe, jour_semaine=self.jour)
        if res['file']:
            await interaction.channel.send(embed=res['embed'], file=res['file'], view=res['view'])
        else:
            await interaction.channel.send(embed=res['embed'])
        await interaction.message.delete()
