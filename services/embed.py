import datetime
import discord

from Button.edt import ButtonsEdt
from models.groupe import Groupe
from models.media import Media
from models.salle import Salle
import services.date as date_service

def obtenir_embed(
        title:str = None,
        description:str = None,
        thumbnail:str = None,
        image:str = None,
        color: discord.Color | int = None,
        url:str = None,
        timestamp:datetime.datetime = None,
        author:dict = None,
        footer:dict = None,
        fields:list[dict] = None
) -> discord.Embed:
    if fields is None:
        fields = []
    embed = discord.Embed(
        title=title,
        description=description,
        color=color,
        colour=color,
        url=url,
        timestamp=timestamp,
    )
    if author:
        embed.set_author(name=author['name'], url=author['url'], icon_url=author['icon_url'])
    if footer:
        embed.set_footer(text=footer['text'], icon_url=footer['icon_url'])
    if image:
        embed.set_image(url=image)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    for field in fields:
        embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
    return embed

def obtenir_edt(entity:Salle | Groupe, premier_jour:datetime.date, dernier_jour:datetime.date, image_edt:Media, bot, ics_url:str):
    embed = obtenir_embed(
        title=f"{entity.__class__.__name__} {entity.nom}\n{date_service.obtenir_format_title_embed(premier_jour, dernier_jour)}",
        thumbnail=bot.user.display_avatar.url,
        author={
            'name': 'Télécharger ICS',
            'url': ics_url,
            'icon_url': None,
        },
        timestamp = datetime.datetime.now(),
    )
    with open(image_edt.path, "rb") as image_file:
        file = discord.File(image_file, filename=image_edt.nom)
        embed.set_image(url=f"attachment://{image_edt.nom}")

    return {
        'embed': embed,
        'file': file,
        'view' : ButtonsEdt(bot, premier_jour, entity, ics_url)
    }

def obtenir_erreur(message:str, thumbnail:str):
    return obtenir_embed(
        title="Erreur",
        description=message,
        thumbnail=thumbnail,
        color=discord.Color.red(),
        timestamp=datetime.datetime.now(),
    )

def obtenir_succes(message:str, thumbnail:str):
    return obtenir_embed(
        title="Succés",
        description=message,
        thumbnail=thumbnail,
        color=discord.Color.green(),
        timestamp=datetime.datetime.now(),
    )