from src.dao.db_connection import DBConnection
from src.Model.user_movie import UserMovie
from dotenv import load_dotenv

class UserMovieDao:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def add_movie(self, id_user, id_film, status):
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

                if existing_row:  # La ligne existe déjà, on met à jour le status
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
                else:  # La ligne n'existe pas, on insère une nouvelle ligne
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





