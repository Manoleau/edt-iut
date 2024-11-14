import os
import sqlite3
from dotenv import load_dotenv
from models.groupe import Groupe

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

    def _execute_query(self, query, params=None, close_cursor=True):
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
            return cursor
        except sqlite3.Error as e:
            print(f'{e}')
            cursor.close()
            return None
    def _insert_many(self, table:str, attributs:list[str], params:list[tuple]):
        try:
            cursor = self.connection.cursor()
            str_attributs = ','.join(attributs)
            str_attributs_values = ','.join(['?' for i in range(len(attributs))])
            query = f"INSERT INTO {table} ({str_attributs}) VALUES ({str_attributs_values})"
            cursor.executemany(query, params)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f'{e}')

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

    def obtenir_groupe_avec_nom(self, nom:str) -> Groupe | None:
        self.connect()
        res = self._fetch_one("SELECT * FROM groupe WHERE nom = ?", (nom,))
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