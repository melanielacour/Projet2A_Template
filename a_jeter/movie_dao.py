import os
import sys

from src.dao.db_connection import DBConnection
from src.Model.film_simple import FilmSimple
from src.utils.singleton import Singleton

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
                    "FROM projet_2a.film         "
                    "WHERE id = %(id_film)s      ",
                    {"id_film": id_film},
                )
                row = cursor.fetchone()
                if row:
                    film= FilmSimple(
                        id_film= row["id"],
                        id_tmdb=row["id_tmdb"],
                        title=["title"]
                    )
                    return film
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
                    "FROM projet_2a.film              "
                    "WHERE id_tmdb = %(id_tmdb)s      ",
                    {"id_tmdb": id_tmdb},
                    
                )
                row = cursor.fetchone()
                if row:
                    film= FilmSimple(
                        id_film= row["id"],
                        id_tmdb=row["id_tmdb"],
                        title=row["title"]
                    )
                    return film
                return None

    def add_local_movie(self,id_tmdb,title):
        """
        Ajoute un film dans la base de données locale
        Paramètre :
        -----------
        film : un objet de la classe Film
        """
        film= self.get_local_movie_by_idtmdb(id_tmdb)
        if film:
            raise ValueError("Film déja présent dans la base de données")
        
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                    cursor.execute(
                    "INSERT INTO projet_2a.film (id_tmdb, title)          "
                    "VALUES (%(id_tmdb)s, %(title)s)                      "
                    "RETURNING id;                                        ",
                    {
                        "id_tmdb": id_tmdb,
                        "title": title
                    },
                    )
                    res1 = cursor.fetchone()
        if res1:
            film= FilmSimple(
                        id_film= res1["id"],
                        id_tmdb=id_tmdb,
                        title=title
                    )
            return True
        return False

            
print(MovieDAO().get_local_movie_by_idtmdb(272025))
