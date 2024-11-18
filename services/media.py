import os
from jinja2 import Environment, FileSystemLoader

from models.logger import Logger
from models.media import Media
from html2image import Html2Image

base_path = 'media'
env = Environment(loader=FileSystemLoader("."))
template_edt = env.get_template("templates/edt.html")
logger = Logger('media_service')

def creer_dossier(path_dossier:str):
    if not os.path.exists(path_dossier):
        os.mkdir(path_dossier)
        logger.ecrire_info(f"Dossier : ${path_dossier} crée avec succés")
creer_dossier(base_path)

def create_html_edt(nom_fichier:str, data:dict, update:bool = True):
    creer_dossier(f"{base_path}/html")
    if not update and os.path.exists(f"{base_path}/html/{nom_fichier}.html"):
        return
    output_html = template_edt.render(data, enumerate=enumerate)

    with open(f"{base_path}/html/{nom_fichier}.html", "w", encoding="utf-8") as file:
        file.write(output_html)
        logger.ecrire_info(f"Fichier EDT HTML : {base_path}/html/{nom_fichier}.html créé avec succés")

def create_image_edt(nom_fichier:str, update:bool = True) -> Media:
    creer_dossier(f"{base_path}/images")
    if not update and os.path.exists(f'{base_path}/images/{nom_fichier}.jpg'):
        return Media(f'{nom_fichier}.jpg', f'{base_path}/images/{nom_fichier}.jpg')
    hti = Html2Image(output_path=f"{base_path}/images")
    hti.screenshot(
        html_file=f'{base_path}/html/{nom_fichier}.html',
        save_as=f'{nom_fichier}.jpg',
        size=(1920, 1080)
    )
    logger.ecrire_info(f"Fichier EDT Image : {base_path}/images/{nom_fichier}.jpg créé avec succés")
    return Media(f'{nom_fichier}.jpg', f'{base_path}/images/{nom_fichier}.jpg')


