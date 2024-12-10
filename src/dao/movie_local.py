from src.dao.db_connection import DBConnection
from src.Model.movie_simple import MovieSimple


class MovieRepo:
    """
    Cette classe permet d'interagir avec
    la table des films de la base de données

    Attributs :
    -----------
    - db_connection : DBConnection
        Instance de la classe DBConnection
        permettant de se connecter à la base de données.
    """

    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def get_movies_by_title(self, title: str) -> list[MovieSimple]:
        """
        Récupère la liste des films ayant le titre spécifié.

        Paramètres :
        -----------
        - title : str
            Le titre du film à rechercher.

        Retourne :
        ---------
        - list[MovieSimple] : Liste d'objets `MovieSimple` contenant les
        films trouvés avec ce titre.
        - None : Si aucun film n'est trouvé pour le titre spécifié.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, id_tmdb, title FROM film WHERE title = %s",
                    (title,)
                )
                rows = cursor.fetchall()
                if rows:
                    return [
                        MovieSimple(
                            id_local=row["id"],
                            id_tmdb=row["id_tmdb"],
                            title=row["title"],
                        )
                        for row in rows
                    ]
                return None

    def get_movie_by_tmdb_id(self, id_tmdb: int) -> MovieSimple:
        """
        Récupère un film en fonction de son identifiant TMDB.

        Paramètres :
        -----------
        - id_tmdb : int
            L'identifiant TMDB du film à récupérer.

        Retourne :
        ---------
        - MovieSimple : Un objet `MovieSimple` contenant les informations
        du film si trouvé.
        - None : Si aucun film ne correspond à l'identifiant TMDB fourni.
        """
        query = "SELECT id, id_tmdb, title FROM film WHERE id_tmdb = %s"
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (id_tmdb,))
                row = cursor.fetchone()
                if row:
                    return MovieSimple(
                        id_local=row["id"],
                        id_tmdb=row["id_tmdb"],
                        title=row["title"]
                    )
                return None

    def get_list_movies(self) -> list[MovieSimple]:
        """
        Récupère la liste de tous les films de la base de données.

        Retourne :
        ---------
        - list[MovieSimple] : Liste d'objets `MovieSimple`
        contenant tous les films disponibles.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, id_tmdb, title FROM film")
                rows = cursor.fetchall()
                return [
                    MovieSimple(
                        id_local=row["id"],
                        id_tmdb=row["id_tmdb"],
                        title=row["title"]
                    )
                    for row in rows
                ]

    def add_movie(self, id_tmdb: int, title: str) -> bool:
        """
        Ajoute un nouveau film à la base de données.

        Paramètres :
        -----------
        - id_tmdb : int
            L'identifiant TMDB du film à ajouter.
        - title : str
            Le titre du film à ajouter.

        Retourne :
        ---------
        - bool : True si le film a été ajouté avec succès, False sinon.
        """
        query1 = "INSERT INTO film (id_tmdb, title) VALUES (%s, %s) RETURNING"
        query = query1 + " id"
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (id_tmdb, title),
                )
                new_id = cursor.fetchone()
                return new_id is not None

    def delete_movie(self, id_local: int) -> bool:
        """
        Supprime un film de la base de données en
        fonction de son identifiant local.

        Paramètres :
        -----------
        - id_local : int
            L'identifiant local du film à supprimer.

        Retourne :
        ---------
        - bool : True si le film a été supprimé avec succès, False sinon.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM film WHERE id = %s RETURNING id", (id_local,)
                )
                deleted_id = cursor.fetchone()
                return deleted_id is not None

    def get_movie_by_id_film(self, id_film: int):
        """
        Récupère un film en fonction de son
        identifiant local dans la table `film`.

        Paramètres :
        -----------
        - id_film : int
            L'identifiant local du film à récupérer.

        Retourne :
        ---------
        - MovieSimple : Un objet `MovieSimple` contenant
        les informations du film si trouvé.
        - None : Si aucun film ne correspond à l'identifiant local fourni.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, id_tmdb, title FROM film WHERE id = %s",
                    (id_film,)
                )
                row = cursor.fetchone()

                if row:
                    return MovieSimple(
                        id_local=row["id"],
                        id_tmdb=row["id_tmdb"],
                        title=row["title"]
                    )
                return None
