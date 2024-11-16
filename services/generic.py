import datetime
import services.embed as embed_service
import services.date as date_service
import services.calendar as calendar_service
import services.media as media_service
from models.groupe import Groupe
from models.jour import Jour
from models.bdd import BDD
from models.salle import Salle
from models.logger import Logger

logger = Logger('generic_service')

def nouveau_commande_edt_salle(bot, salle_id:str):
    bdd = BDD()
    salle = bdd.obtenir_salle_avec_id(salle_id)
    res = nouveau_commande_edt(bot, salle, with_groupe=True)
    return res
def nouveau_commande_edt_groupe(bot, groupe_id:str):
    bdd = BDD()
    groupe = bdd.obtenir_groupe_avec_id(groupe_id)
    res = nouveau_commande_edt(bot,groupe, with_groupe=False)
    return res

def nouveau_commande_edt(bot, entity:Groupe | Salle | None, with_groupe=False):
    if entity:
        setup = obtenir_setup(entity, with_groupe)
        if setup['erreur'] is None:
            jours = setup['jours']
            premier_jour = setup['premier_jour']
            dernier_jour = setup['dernier_jour']
            horaires_tries = setup['horaires_tries']
            cal = setup['cal']
            data = {
                'jours': [Jour(i) for i in range(len(jours))],
                'heures': horaires_tries,
                'vide': len(horaires_tries) == 0
            }
            nom_fichier = f'{entity.nom.lower()}_{premier_jour.strftime('%Y-%m-%d')}_{dernier_jour.strftime('%Y-%m-%d')}'.replace(
                " ", "")
            media_service.create_html_edt(nom_fichier, data)
            image = media_service.create_image_edt(nom_fichier)
            res = embed_service.obtenir_edt(entity, premier_jour, dernier_jour, image, bot.user.display_avatar.url, cal['ics'])
        else:
            res = {
                'embed': embed_service.obtenir_erreur(setup['erreur'], bot.user.display_avatar.url),
                'file': None
            }
    else:
        logger.ecrire_error('Aucun résultat')
        res = {
            'embed': embed_service.obtenir_erreur(f"Aucun résultat", bot.user.display_avatar.url),
            'file': None
        }
    return res

def obtenir_setup(entity: Salle | Groupe, with_groupe:bool = False):
    jours = date_service.obtenir_jour_semaine_actuel()
    premier_jour = jours[0]
    dernier_jour = jours[4]
    cal = calendar_service.obtenir(entity.id, premier_jour, dernier_jour)
    if cal['ics'] is None:

        return {
            'erreur' : cal['erreur'],
        }
    heure_decalage = date_service.obtenir_heure_decalage()
    horaires = []
    check_horaires = []
    indices_horaires = {}
    for event in cal['events']:
        event.begin += datetime.timedelta(hours=heure_decalage)
        event.end += datetime.timedelta(hours=heure_decalage)
        horaire = f"{event.begin.strftime('%H:%M')} - {event.end.strftime('%H:%M')}"
        if horaire not in check_horaires:
            horaires.append({
                'time': horaire,
                'cours': []
            })
            check_horaires.append(horaire)
    horaires_tries = sorted(horaires, key=lambda x: datetime.datetime.strptime(x['time'].split(' - ')[0], '%H:%M'))
    for i in range(len(horaires_tries)):
        indices_horaires[horaires_tries[i]['time']] = {
            'indice': i
        }
    for jour in jours:
        for event in cal['events']:
            if jour.day == event.begin.date().day:
                horaire = f"{event.begin.strftime('%H:%M')} - {event.end.strftime('%H:%M')}"
                for i in range(jour.weekday() - len(horaires_tries[indices_horaires[horaire]['indice']]['cours'])):
                    horaires_tries[indices_horaires[horaire]['indice']]['cours'].append('-')
                description = [item for item in event.description.split("\n") if item]
                if with_groupe:
                    groupe = description[0]
                    prof = description[1]
                    try:
                        int(groupe)
                        groupe = description[1]
                        horaires_tries[indices_horaires[horaire]['indice']]['cours'].append(f'{event.name}<br>{groupe}')
                    except ValueError:
                        horaires_tries[indices_horaires[horaire]['indice']]['cours'].append(f'{event.name}<br>{groupe}<br>{prof}')
                else:
                    try:
                        int(description[0])
                        horaires_tries[indices_horaires[horaire]['indice']]['cours'].append(f'{event.name}')
                    except ValueError:
                        prof = description[1]
                        horaires_tries[indices_horaires[horaire]['indice']]['cours'].append(f'{event.name}<br>{prof}')

    for horaire in horaires_tries:
        while len(horaire['cours']) < 5:
            horaire['cours'].append('-')

    return {
        'jours': jours,
        'premier_jour': premier_jour,
        'dernier_jour': dernier_jour,
        'horaires_tries': horaires_tries,
        'cal' : cal,
        'erreur': None
    }
