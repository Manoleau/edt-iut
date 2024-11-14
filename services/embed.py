import datetime
import discord
from discord.ext import commands
from discord import app_commands


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