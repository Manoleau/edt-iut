from models.bdd import BDD
from models.type_salle import TypeSalle
import time
import json

file_path = "data.json"

debut = time.time()
bdd = BDD()
bdd.connect()
bdd._execute_query("""
    CREATE TABLE IF NOT EXISTS groupe (
        id VARCHAR(255) PRIMARY KEY,
        nom VARCHAR(255) NOT NULL
    );""")
bdd._execute_query("""
        CREATE TABLE IF NOT EXISTS salle (
            id VARCHAR(255) PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            type VARCHAR(255) NOT NULL
        );""")
fin = time.time()
print(f"Durée création tables : {fin-debut:.3f}s")


debut = time.time()
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

bdd._insert_many('salle', ['id', 'nom', 'type'], [(salle['id'], salle['nom'], TypeSalle(salle['type'].lower()).name) for salle in data["salle"]])
bdd._insert_many('groupe', ['id', 'nom'], [(groupe['id'], groupe['nom']) for groupe in data["groupe"]])
fin = time.time()
print(f"Durée remplissage tables : {fin-debut:.3f}s")
bdd.disconnect()