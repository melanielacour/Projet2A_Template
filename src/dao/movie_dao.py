import os
import sys

from Film import Film

from dao.db_connection import DBConnection
from utils.singleton import Singleton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class MovieDAO(metaclass=Singleton):
    def get_local_movie(self, id_film: int):
        """
        Récupère le nom du film à partir de son ID.
        Paramètre:
        ---------
         id_film:  L'ID du film à rechercher.
        Return:
        -------
        Une instance de UserSimple avec le titre du film,
                ou None si le film n'existe pas.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT title   "
                    "FROM movies    "
                    "WHERE id = %s", (id_film,))
                row = cursor.fetchone()
                if row:
                    return Film(
                        title=row["title"]
                    )
                return None
