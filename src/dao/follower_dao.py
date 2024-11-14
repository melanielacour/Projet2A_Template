from src.dao.db_connection import DBConnection
from src.dao.user_repo import UserRepo


class FollowerDao:
    """
    Cette classe permet de gérer les followers dans la base de données
    des followers. Elle représente les interractions entre les utilisateurs

    Attribut :
    -----------

    db_connection : DBConnection
        Une instance de DBCOnnection qui permet la connexion

    Méthodes :
    ----------

    follow_scout : Permet de suivre un éclaireur
    unfollow_scout : Permet de ne plus suivre un éclaireur
    get_scouts_followed_by_user : Récupère la liste des éclaireurs
        d'un utilisateur
    get_followers_of_scout : Récupère la liste des utilisateurs qui
        suivent un éclaireur
    get_watchlist_of_scouts : récupère la watchlist d'un éclaireur
    """
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def follow_scout(self, id_follower, id_scout):
        """Permet à un utilisateur de suivre un éclaireur

        Attributs:
        ----------

        id_follower : int
            L'idedntifiant de l'utilisateur suivi
        id_scout : int
            L'identifiant de l'éclaireur
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO projet_2a.followers (id_follower, id_scout)
                    VALUES (%(id_follower)s, %(id_scout)s)
                    ON CONFLICT (id_follower, id_scout) DO NOTHING;
                    """,
                    {"id_follower": id_follower, "id_scout": id_scout}
                )
                return True

    def unfollow_scout(self, id_follower, id_scout):
        """Permet à un utilisateur de ne plus suivre un éclaireur

        Attributs:
        ----------

        id_follower : int
            L'idedntifiant de l'utilisateur suivi
        id_scout : int
            L'identifiant de l'éclaireur
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM projet_2a.followers
                    WHERE id_follower = %(id_follower)s AND id_scout = %(id_scout)s;
                    """,
                    {"id_follower": id_follower, "id_scout": id_scout}
                )
                return True

    def get_scouts_followed_by_user(self, id_follower):
        """Récupère la liste des éclaireurs suivis par un utilisateur
        Attribut:
        ----------

        id_follower : int
            L'idedntifiant de l'utilisateur suivi

        Return:
        -------

        :list
            La liste des éclaireurs
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT scouts.id_user FROM projet_2a.followers
                    JOIN projet_2a.scouts ON scouts.id_user = followers.id_scout
                    WHERE followers.id_follower = %(id_follower)s;
                    """,
                    {"id_follower": id_follower}
                )
                rows = cursor.fetchall()

        return [row["id_user"] for row in rows]

    def get_followers_of_scout(self, id_scout):
        """Récupère la liste des utilisateurs qui suivent un éclaireur

        Attribut:
        ----------

        id_scout : int
            L'identifiant de l'éclaireur

        Return :
        --------
        : list
            La liste des utilisateurs
        """
        user = UserRepo(DBConnection()).get_by_id(id_scout)
        if not user.is_scout:
            raise ValueError("Vous n'êtes pas éclaireur !")
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id_follower FROM projet_2a.followers
                    WHERE id_scout = %(id_scout)s;
                    """,
                    {"id_scout": id_scout}
                )
                rows = cursor.fetchall()

        return [row["id_follower"] for row in rows]

    def get_watchlist_of_scouts(self, id_follower, id_scout):
        """
        Récupère la watchlist d'un éclaireurs suivi par un utilisateur

        Attributs:
        ----------

        id_follower : int
            L'idedntifiant de l'utilisateur suivi
        id_scout : int
            L'identifiant de l'éclaireur

        Return :
        --------

         :list
            La watchlist de l'éclaireur demandé
        """

        # Vérification que l'utilisateur suit l'éclaireur
        scouts_suivis = self.get_scouts_followed_by_user(id_follower)
        if id_scout not in scouts_suivis:
            raise ValueError("Vous ne suivez pas cet éclaireur")

        # Récupération de la watchlist de l'éclaireur suivi
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT DISTINCT films.id, films.title
                    FROM projet_2a.followers
                    JOIN projet_2a.user_movies ON user_movies.id_user = followers.id_scout
                    JOIN projet_2a.films ON films.id = user_movies.id_film
                    WHERE followers.id_follower = %(id_follower)s
                    AND user_movies.status = 'to_watch'
                    AND followers.id_scout = %(id_scout)s;
                    """,
                    {"id_follower": id_follower, "id_scout": id_scout}
                )
                rows = cursor.fetchall()

        # Retourner la liste des films à regarder (watchlist) sous forme de dictionnaires
        return [{"id": row["id"], "title": row["title"]} for row in rows]
