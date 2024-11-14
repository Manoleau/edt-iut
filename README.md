# edt-iut
![logo](https://www.aht.li/3815097/logo_EDTIUT_1.png)

# Installation
### Prérequis
- Docker
- Git
### Clonage
```
git clone https://github.com/Manoleau/edt-iut.git
```
### Env
- Créez un fichier .env à la racine du projet
- Ajoutez les lignes suivantes dans le fichier
- Changez le token par votre token de bot
```
TOKEN_DISCORD_BOT=ChangerToken
DB_NAME=data_base
```
### Docker
```
docker-compose up
```

# Commandes
- edt
    * paramètre
        1. classe (nom de la classe).
    * Renvoie l'emploi du temps de la classe selectionné de la semaine actuelle.
  
![edt](https://www.aht.li/3815096/commandeedt_2.png)

- salle libre
  * paramètres
      1. type (type de la salle (Info, TD, Réseau, Autre))
      2. jour (les salles libre de ce jour)
  * Renvoie toutes les salles libres et leurs créneaux (8h-10h, 8h-14h, etc...).

![sallelibre](https://www.aht.li/3815099/commandesallelibre_1.png)

- edt salle
    * paramètre
        1. salle (nom de la salle)
    * Renvoie l'emploi du temps de la salle selectionné de la semaine actuelle.

![edtsalle](https://www.aht.li/3815100/commandeedtsalle_1.png)
