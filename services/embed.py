import datetime
import discord

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


def obtenir_edt_salle(salle: Salle, premier_jour:datetime.date, dernier_jour:datetime.date, image_edt:Media, thumbnail:str, ics_url:str):
    return obtenir_edt(
        f"Salle {salle.nom}\n{date_service.obtenir_format_embed(premier_jour, dernier_jour)}",
        image_edt,
        thumbnail,
        ics_url,
    )

def obtenir_edt_groupe(groupe: Groupe, premier_jour:datetime.date, dernier_jour:datetime.date, image_edt:Media, thumbnail:str, ics_url:str):
    return obtenir_edt(
        f"Groupe {groupe.nom}\n{date_service.obtenir_format_embed(premier_jour, dernier_jour)}",
        image_edt,
        thumbnail,
        ics_url,
    )

def obtenir_edt(titre:str, image_edt:Media, thumbnail:str, ics_url:str):
    embed = obtenir_embed(
        title=titre,
        thumbnail=thumbnail,
        author={
            'name': 'Télécharger ICS',
            'url': ics_url,
            'icon_url': None,
        }
    )
    with open(image_edt.path, "rb") as image_file:
        file = discord.File(image_file, filename=image_edt.nom)
        embed.set_image(url=f"attachment://{image_edt.nom}")

    return {
        'embed': embed,
        'file': file,
    }