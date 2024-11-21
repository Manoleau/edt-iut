import os
import sqlite3
from typing import Any

from dotenv import load_dotenv
from models.groupe import Groupe
from models.salle import Salle
from models.type_salle import TypeSalle

load_dotenv()

class BDD:
    def __init__(self):
        """
        Initialise la connexion à la base de données SQLite.
        """
        self.db_name = f"{os.getenv("DB_NAME")}.db"
        self.connection = None

    def connect(self):
        """
        Ouvre la connexion à la base de données.
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("Connexion à la base de données réussie.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion : {e}")

    def disconnect(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.connection:
            self.connection.close()
            print("Connexion à la base de données fermée.")

    def _execute_query(self, query, params=None, close_cursor=True) -> Any | bool:
        """
        Exécute une requête SQL.
        :param query: La requête SQL à exécuter.
        :param params: Les paramètres de la requête SQL (facultatif).
        :return: Le curseur de la requête.
        """
        try:

            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            if close_cursor:

                cursor.close()

                return True
            return cursor
        except sqlite3.Error as e:
            print(f'{e}')
            cursor.close()

            return False
    def _insert_many(self, table:str, attributs:list[str], params:list[tuple]) -> bool:
        try:

            cursor = self.connection.cursor()
            str_attributs = ','.join(attributs)
            str_attributs_values = ','.join(['?' for i in range(len(attributs))])
            query = f"INSERT INTO {table} ({str_attributs}) VALUES ({str_attributs_values})"
            cursor.executemany(query, params)
            self.connection.commit()

            return True
        except sqlite3.Error as e:
            print(f'{e}')

            return False

    def _insert_one(self, table:str, attributs:list[str], params:tuple) -> bool:
        try:

            cursor = self.connection.cursor()
            str_attributs = ','.join(attributs)
            str_attributs_values = ','.join(['?' for i in range(len(attributs))])
            query = f"INSERT INTO {table} ({str_attributs}) VALUES ({str_attributs_values})"
            cursor.execute(query, params)
            self.connection.commit()

            return True
        except sqlite3.Error as e:
            print(f'{e}')

            return False

    def _fetch_all(self, query, params=None):
        """
        Récupère tous les résultats d'une requête SQL.
        :param query: La requête SQL à exécuter.
        :param params: Les paramètres de la requête SQL (facultatif).
        :return: Une liste de tuples contenant les résultats.
        """
        cursor = self._execute_query(query, params, False)
        if cursor:
            results = cursor.fetchall()
            cursor.close()
            return results
        return []

    def _fetch_one(self, query, params=None):
        """
        Récupère un seul résultat d'une requête SQL.
        :param query: La requête SQL à exécuter.
        :param params: Les paramètres de la requête SQL (facultatif).
        :return: Un tuple contenant le résultat.
        """
        cursor = self._execute_query(query, params, False)
        if cursor:
            result = cursor.fetchone()
            cursor.close()
            return result
        return None

    def _delete(self, table, attributs:list[str] = [], params:tuple = None):
        try:
            query = f"DELETE FROM {table}"
            if len(attributs) == 0:
                query += ";"
                params = None
            else:
                condition = ""
                for i in range(len(attributs)):
                    attribut = attributs[i]
                    if i == len(attributs) - 1:
                        condition += f"{attribut} = ?;"
                    else:
                        condition += f"{attribut} = ? AND "
                query += f" WHERE {condition}"
            cursor = self._execute_query(query, params, close_cursor=False)
            if cursor:
                return cursor.rowcount > 0
            return cursor
        except sqlite3.Error as e:
            print(f'{e}')
            return False
    def obtenir_groupe_avec_nom(self, nom:str) -> Groupe | None:
        self.connect()
        res = self._fetch_one("SELECT * FROM groupe WHERE nom = ?;", (nom,))
        self.disconnect()
        if res:
            return Groupe(
                res[0],
                res[1]
            )
        return None

    def obtenir_groupe_avec_id(self, id: str) -> Groupe | None:
        self.connect()
        res = self._fetch_one("SELECT * FROM groupe WHERE id = ?", (id,))
        self.disconnect()
        if res:
            return Groupe(
                res[0],
                res[1]
            )
        return None

    def obtenir_salle_avec_nom(self, nom: str) -> Salle | None:
        self.connect()
        res = self._fetch_one("SELECT * FROM salle WHERE nom = ?", (nom,))
        self.disconnect()
        if res:
            return Salle(
                res[0],
                res[1],
                TypeSalle[res[2].upper()]
            )
        return None

    def obtenir_salle_avec_id(self, id: str) -> Salle | None:
        self.connect()
        res = self._fetch_one("SELECT * FROM salle WHERE id = ?", (id,))
        self.disconnect()
        if res:
            return Salle(
                res[0],
                res[1],
                TypeSalle[res[2].upper()]
            )
        return None

    def obtenir_toutes_salles(self, order_by:str = "nom") -> list[Salle]:
        self.connect()
        res = self._fetch_all(f"SELECT * FROM salle ORDER BY {order_by};")
        self.disconnect()
        return [Salle(salle[0], salle[1], TypeSalle[salle[2].upper()]) for salle in res]

    def obtenir_tous_groupes(self, order_by:str = "nom") -> list[Groupe]:
        self.connect()
        res = self._fetch_all(f"SELECT * FROM groupe ORDER BY {order_by};")
        self.disconnect()
        return [Groupe(groupe[0], groupe[1]) for groupe in res]