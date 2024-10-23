import os
import sys

from Film import Film

from dao.db_connection import DBConnection
from src.Model.film_simple import FilmSimple
from utils.singleton import Singleton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class MovieDAO(metaclass=Singleton):
    def get_local_movie_by_id(self, id_film: int):
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
                    {"id_film": id_film},
                )
                row = cursor.fetchone()
                if row:
                    film= FilmSimple(
                        id_film= row["id_film"],
                        id_tmdb=row["id_tmdb"],
                        title=["title"]
                    )
                    return row
                return None

    def get_local_movie_by_idtmdb(self, id_tmdb:int):
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
                    "SELECT *                         "
                    "FROM movies                      "
                    "WHERE id_tmdb = %(id_tmdb)s      ",
                    {"id_tmdb": id_tmdb},
                    
                )
                row = cursor.fetchone()
                if row:
                    film= FilmSimple(
                        id_film= row["id_film"],
                        id_tmdb=row["id_tmdb"],
                        title=["title"]
                    )
                    return row
                return None

    def add_local_movie(self,title,id_tmdb):
        """
        Ajoute un film dans la base de données locale
        Paramètre :
        -----------
        film : un objet de la classe Film
        """
        film= self.get_local_movie_by_title()
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
