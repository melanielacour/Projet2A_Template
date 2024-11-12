from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.Model.user_movie import UserMovie


class UserMovieDao:
    """
    Cette classe permet de gérer la base de données des films en les
    enregistrant dans la table user_movies, qui représente
    les relations entre les utilisateurs et les films."""

    def __init__(self, db_connection: DBConnection):
        # On établit une connexion avec la BDD
        self.db_connection = db_connection

    def add_movie(self, id_user, id_film, status):
         """
        Méthode qui ajoute une relation entre un utilisateur et un film, ou
        met à jour le statut si cette relation existe déjà.

        Parameters:
        -----------
        id_user : int
            L'identifiant de l'utilisateur.
        id_film : int
            L'identifiant du film dans la base de données.
        status : str
            Le statut de la relation entre l'utilisateur et le film.

        - Si une relation existe déjà entre l'utilisateur et le film, le statut est mis à jour.
        - Sinon, une nouvelle relation est insérée dans la base de données.
        """
        # Vérifie d'abord si une ligne correspondante existe
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 1 FROM projet_2a.user_movies
                    WHERE id_user = %(id_user)s AND id_film = %(id_film)s;
                    """,
                    {
                        "id_user": id_user,
                        "id_film": id_film
                    }
                )
                existing_row = cursor.fetchone()

                if existing_row: # si la ligne existe déjà, on met à jour le status
                    cursor.execute(
                        """
                        UPDATE projet_2a.user_movies
                        SET status = %(status)s
                        WHERE id_user = %(id_user)s AND id_film = %(id_film)s;
                        """,
                        {
                            "id_user": id_user,
                            "id_film": id_film,
                            "status": status
                        }
                    )
                else:  # si la ligne n'existe pas, on insère une nouvelle ligne
                    cursor.execute(
                        """
                        INSERT INTO projet_2a.user_movies (id_user, id_film, status)
                        VALUES (%(id_user)s, %(id_film)s, %(status)s);
                        """,
                        {
                            "id_user": id_user,
                            "id_film": id_film,
                            "status": status
                        }
                    )


    def get_movies_by_user(self, id_user, status=None):
        """
        Méthode qui récupère les films associés à un utilisateur.

        Parameters:
        -----------
        id_user : int
            L'identifiant de l'utilisateur.
        status : str, optionnel
            Le statut à filtrer. Si aucun statut n'est précisé,
            tous les films de l'utilisateur sont retournés.

        Returns:
        ---------
        list[UserMovie]
            Une liste d'objets UserMovie représentant les films de l'utilisateur avec le statut donné.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id_user, id_film, status FROM projet_2a.user_movies WHERE id_user = %(id_user)s"
                params = {"id_user": id_user}

                if status:
                    query += " AND status = %(status)s"
                    params["status"] = status

                cursor.execute(query, params)
                rows = cursor.fetchall()

        return [UserMovie(row["id_user"], row["id_film"], row["status"]) for row in rows]

    def delete_movie(self, id_user, id_film, status):
        """
        Supprime la relation entre un utilisateur et un film avec un statut spécifique.

        Parameters:
        -----------
        id_user : int
            L'identifiant unique de l'utilisateur.
        id_film : int
            L'identifiant unique du film.
        status : str
            Le statut de la relation à supprimer.

        Returns:
        ---------
        bool
            Retourne True si la suppression a été effectuée.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM projet_2a.user_movies
                    WHERE id_user = %(id_user)s AND id_film = %(id_film)s AND status = %(status)s;
                    """,
                    {"id_user": id_user, "id_film": id_film, "status": status}
                )
                return True
