from models.type_salle import TypeSalle

class Salle:
    def __init__(self, id_salle:str, nom_salle:str, type_salle:TypeSalle):
        self.nom = nom_salle
        self.id = id_salle
        self.type = type_salle
