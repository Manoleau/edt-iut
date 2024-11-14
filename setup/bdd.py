from models.bdd import BDD
from models.type_salle import TypeSalle
import time
def creer_tables():
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
    bdd.disconnect()
    fin = time.time()
    print(f"Durée création tables : {fin-debut:.2f}s")


def remplir_tables():
    debut = time.time()
    bdd = BDD()
    bdd.connect()
    data_salle = [
        ('9113', 'S04', TypeSalle.AUTRE.name),
        ('126', 'S18', TypeSalle.RESEAU.name),
        ('134', 'S21', TypeSalle.AUTRE.name),
        ('132', 'S23', TypeSalle.RESEAU.name),
        ('118', 'S01', TypeSalle.INFO.name),
        ('119', 'S03', TypeSalle.INFO.name),
        ('120', 'S13', TypeSalle.INFO.name),
        ('121', 'S14', TypeSalle.INFO.name),
        ('122', 'S16', TypeSalle.INFO.name),
        ('123', 'S17', TypeSalle.INFO.name),
        ('135', 'S22', TypeSalle.INFO.name),
        ('136', 'S24', TypeSalle.INFO.name),
        ('133', 'S26', TypeSalle.INFO.name),
        ('9188', 'S27', TypeSalle.INFO.name),
        ('344', '040', TypeSalle.TD.name),
        ('127', 'S10', TypeSalle.TD.name),
        ('128', 'S11', TypeSalle.TD.name),
        ('129', 'S12', TypeSalle.TD.name),
        ('130', 'S15', TypeSalle.TD.name),
        ('131', 'S25', TypeSalle.TD.name)
    ]
    data_groupe = [
        ('6161', 'BUT3 RA1A'),
        ('6163', 'BUT3 RA1B'),
        ('6165', 'BUT3 RA2A'),
        ('6168', 'BUT3 RA2B'),
        ('14059', 'BUT3 RA3'),
        ('6048', 'BUT3 AGED'),
        ('6136', 'BUT3 DACS'),
    ]
    bdd._insert_many('salle', ['id', 'nom', 'type'], data_salle)
    bdd._insert_many('groupe', ['id', 'nom'], data_groupe)
    bdd.disconnect()
    fin = time.time()
    print(f"Durée remplissage tables : {fin-debut:.2f}s")