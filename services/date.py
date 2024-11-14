import datetime
import pytz

from models.jour import Jour
from models.mois import Mois


def obtenir_jour_semaine_actuel() -> list[datetime.date]:
    aujourdhui = datetime.date.today()
    lundi = aujourdhui - datetime.timedelta(days=aujourdhui.weekday())
    mardi = aujourdhui + datetime.timedelta(days=1 - aujourdhui.weekday() % 7)
    mercredi = aujourdhui + datetime.timedelta(days=2 - aujourdhui.weekday() % 7)
    jeudi = aujourdhui + datetime.timedelta(days=3 - aujourdhui.weekday() % 7)
    vendredi = aujourdhui + datetime.timedelta(days=4 - aujourdhui.weekday() % 7)
    if aujourdhui.weekday() == 5 or aujourdhui.weekday() == 6:
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


def obtenir_indice_horaire(horaires:list[dict], horaire:str):
    res = -1
    i = 0
    while res == -1 and i < len(horaires):
        if horaires[i]['time'] == horaire:
            res = i
        i += 1
    return res

def obtenir_format_embed(premier_jour:datetime.date, dernier_jour:datetime.date):
    return f"{Jour(premier_jour.weekday()).name.capitalize()} {premier_jour.day} {Mois(premier_jour.month).name.capitalize()} {premier_jour.year}\n{Jour(dernier_jour.weekday()).name.capitalize()} {dernier_jour.day} {Mois(dernier_jour.month).name.capitalize()} {dernier_jour.year}"