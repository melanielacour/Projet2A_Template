from src.dao.db_connection import DBConnection
from src.Model.follower import Follower

class FollowerDao:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def follow_scout(self, id_follower, id_scout):
        """Permet à un utilisateur de suivre un éclaireur"""
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
        """Permet à un utilisateur de ne plus suivre un éclaireur"""
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
        """Récupère la liste des éclaireurs suivis par un utilisateur"""
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
        """Récupère la liste des utilisateurs qui suivent un éclaireur"""
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

    def get_watchlist_of_scouts(self, id_follower):
        """Récupère la watchlist de tous les éclaireurs suivis par un utilisateur"""
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT DISTINCT films.id, films.title
                    FROM projet_2a.followers
                    JOIN projet_2a.user_movies ON user_movies.id_user = followers.id_scout
                    JOIN projet_2a.films ON films.id = user_movies.id_film
                    WHERE followers.id_follower = %(id_follower)s AND user_movies.status = 'to_watch';
                    """,
                    {"id_follower": id_follower}
                )
                rows = cursor.fetchall()

        return [{"id": row["id"], "title": row["title"]} for row in rows]
