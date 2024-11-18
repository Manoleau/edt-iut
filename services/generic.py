import datetime
import services.embed as embed_service
import services.date as date_service
import services.calendar as calendar_service
import services.media as media_service
from models.groupe import Groupe
from models.bdd import BDD
from models.couleurs import Couleurs
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
            premier_jour = setup['premier_jour']
            dernier_jour = setup['dernier_jour']
            cours = setup['cours']
            cal = setup['cal']
            data = {
                'cours': cours,
                'vide': len(cours) == 0
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

    ## Il faut nom (deja fait), grid-column (Jour) et grid-row (Heure départ calcul + durée)
    jours = date_service.obtenir_jour_semaine_actuel()
    premier_jour = jours[0]
    dernier_jour = jours[4]
    cal = calendar_service.obtenir(entity.id, premier_jour, dernier_jour)
    if cal['ics'] is None:
        return {
            'erreur' : cal['erreur'],
        }
    heure_decalage = date_service.obtenir_heure_decalage()
    liste_cours = []
    liste_cours_colors = {

    }
    liste_couleurs = list(Couleurs)
    current_couleur_index = 0
    for event in cal['events']:
        event.begin += datetime.timedelta(hours=heure_decalage)
        event.end += datetime.timedelta(hours=heure_decalage)
        debut_datetime = event.begin.datetime
        description = [item for item in event.description.split("\n") if item]
        if with_groupe:
            groupe = description[0]
            prof = description[1]
            try:
                int(groupe)
                groupe = description[1]
                nom = f'{event.name}<br>{groupe}<br>{event.location}'
            except ValueError:
                nom = f'{event.name}<br>{groupe}<br>{prof}<br>{event.location}'
        else:
            try:
                int(description[0])
                nom = f'{event.name}<br>{event.location}'
            except ValueError:
                prof = description[1]
                nom = f'{event.name}<br>{prof}<br>{event.location}'
        cle_nom = normaliser_cle(event.name)
        if cle_nom in liste_cours_colors:
            couleur = liste_cours_colors[cle_nom]
        else:
            couleur = liste_couleurs[current_couleur_index]
            liste_cours_colors[cle_nom] = couleur
            current_couleur_index += 1

        liste_cours.append({
            'nom' : nom,
            'style' : f"background-color: {couleur.value}; grid-column: {event.begin.date().weekday() + 2}; {_calcule_grid_row(debut_datetime.hour, debut_datetime.minute, event.duration.seconds // 60 // 60)}",
        })
    return {
        'premier_jour': premier_jour,
        'dernier_jour': dernier_jour,
        'cal' : cal,
        'cours' : liste_cours,
        'erreur': None,
    }

def _calcule_grid_row(heure_debut:int, minute_debut:int, duree:int):
    debut_grid = (heure_debut - 8) * 2 + 1
    if minute_debut == 30:
        debut_grid += 1
    return f"grid-row: {debut_grid} / span {duree * 2};"

import re

def normaliser_cle(cle):
    cle = cle.lower()
    cle = cle.replace(" ", "_")
    cle = re.sub(r"[^a-z0-9_]", "", cle)
    return cle