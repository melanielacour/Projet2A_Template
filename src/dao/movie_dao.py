import os
import sys

from Film import Film

from dao.db_connection import DBConnection
from src.Model.film_simple import FilmSimple
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
                    "SELECT *                    "
                    "FROM movies                 "
                    "WHERE id = %(id_film)s      ",
                )
                row = cursor.fetchone()
                if row:
                    film= FilmSimple(
                        id_film= row["id_film"]

                    )
                    return row
                return None

    def add_local_movie(self, film):
        """
        Ajoute un film dans la base de données locale
        Paramètre :
        -----------
        film : un objet de la classe Film
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                try:
                    cursor.execute(
                        """
                     INSERT INTO movies (id_film,title,producer,category,date)
                        VALUES (%s, %s, %s, %s, %s)
                     """,
                        (film.id_film, film.title, film.producer, film.category, film.date)
                     )
                    connection.commit()
                except Exception as e:
                    print(f"Erreur dans l'ajout dans la base de donneés de : {e}")
                    connection.rollback()
