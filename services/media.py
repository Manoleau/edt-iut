from jinja2 import Environment, FileSystemLoader
import imgkit
import os
from models.media import Media
from models.logger import Logger

base_path = 'media'
env = Environment(loader=FileSystemLoader("."))
template_edt = env.get_template("templates/edt.html")
logger = Logger('media_service')
options_image = {
    'width': 1920,
    'height': 1080,
}

def creer_dossier(path_dossier:str):
    if not os.path.exists(path_dossier):
        os.mkdir(path_dossier)
        logger.ecrire_info(f"Dossier : ${path_dossier} crée avec succés")
creer_dossier(base_path)

def create_html_edt(nom_fichier:str, data:dict) -> str:
    output_html = template_edt.render(data, enumerate=enumerate)
    creer_dossier(f"{base_path}/html")
    with open(f"{base_path}/html/{nom_fichier}.html", "w", encoding="utf-8") as file:
        file.write(output_html)
        logger.ecrire_info(f"Fichier EDT HTML : {base_path}/html/{nom_fichier}.html créé avec succés")
    return output_html

def create_image_edt(nom_fichier:str) -> Media:
    creer_dossier(f"{base_path}/images")
    imgkit.from_file(f'{base_path}/html/{nom_fichier}.html', f'{base_path}/images/{nom_fichier}.jpg', options=options_image)
    logger.ecrire_info(f"Fichier EDT Image : {base_path}/images/{nom_fichier}.jpg créé avec succés")
    return Media(f'{nom_fichier}.jpg', f'{base_path}/images/{nom_fichier}.jpg')


