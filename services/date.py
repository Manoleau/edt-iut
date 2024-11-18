import datetime
import pytz

from models.jour import Jour
from models.mois import Mois


def obtenir_jour_semaine_actuel(jour:datetime.date = None) -> list[datetime.date]:
    if jour is None:
        jour = datetime.date.today()
    lundi = jour - datetime.timedelta(days=jour.weekday())
    mardi = jour + datetime.timedelta(days=1 - jour.weekday() % 7)
    mercredi = jour + datetime.timedelta(days=2 - jour.weekday() % 7)
    jeudi = jour + datetime.timedelta(days=3 - jour.weekday() % 7)
    vendredi = jour + datetime.timedelta(days=4 - jour.weekday() % 7)
    if jour.weekday() == 5 or jour.weekday() == 6:
        lundi = lundi + datetime.timedelta(days=7)
        mardi = mardi + datetime.timedelta(days=7)
        mercredi = mercredi + datetime.timedelta(days=7)
        jeudi = jeudi + datetime.timedelta(days=7)
        vendredi = vendredi + datetime.timedelta(days=7)
    return [lundi, mardi, mercredi, jeudi, vendredi]

def obtenir_heure_decalage(zone:str = "Europe/Paris"):
    local_timezone = pytz.timezone(zone)
    local_time = datetime.datetime.now(local_timezone)
    return int(local_time.utcoffset().total_seconds() / 3600)

def obtenir_format_title_embed(premier_jour:datetime.date, dernier_jour:datetime.date):
    return f"{Jour(premier_jour.weekday()).name.capitalize()} {premier_jour.day} {Mois(premier_jour.month).name.capitalize()} {premier_jour.year}\n{Jour(dernier_jour.weekday()).name.capitalize()} {dernier_jour.day} {Mois(dernier_jour.month).name.capitalize()} {dernier_jour.year}"