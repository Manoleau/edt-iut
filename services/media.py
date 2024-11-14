from jinja2 import Environment, FileSystemLoader
import imgkit

from models.media import Media

base_path = "media"
env = Environment(loader=FileSystemLoader("."))
template_edt = env.get_template("templates/edt.html")
options = {
    'width': 1920,
    'height': 1080,
}
def create_html_edt(nom_fichier:str, data:dict) -> str:
    output_html = template_edt.render(data, enumerate=enumerate)
    with open(f"{base_path}/html/{nom_fichier}.html", "w", encoding="utf-8") as file:
        file.write(output_html)
    return output_html

def create_image_edt(nom_fichier:str):
    imgkit.from_file(f'{base_path}/html/{nom_fichier}.html', f'{base_path}/images/{nom_fichier}.jpg', options=options)
    return Media(f'{nom_fichier}.jpg', f'{base_path}/images/{nom_fichier}.jpg')

def create_media():
    return

def delete_media():
    return