from src.dao.db_connection import DBConnection
from src.Model.movie_simple import MovieSimple


class MovieRepo:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def get_movies_by_title(self, title: str) -> list[MovieSimple]:
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, id_tmdb, title FROM film WHERE title = %s", (title,))
                rows = cursor.fetchall()
                if rows:
                    return [MovieSimple(id_local=row["id"], id_tmdb=row["id_tmdb"], title=row["title"]) for row in rows]
                return None

    def get_movie_by_tmdb_id(self, id_tmdb: int) -> MovieSimple:
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, id_tmdb, title FROM film WHERE id_tmdb = %s", (id_tmdb,))
                row = cursor.fetchone()
                if row:
                    return MovieSimple(id_local=row["id"], id_tmdb=row["id_tmdb"], title=row["title"])
                return None

    def list_movies(self) -> list[MovieSimple]:
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, id_tmdb, title FROM film")
                rows = cursor.fetchall()
                return [MovieSimple(id_local=row["id"], id_tmdb=row["id_tmdb"], title=row["title"]) for row in rows]

    def add_movie(self, id_tmdb: int, title: str) -> bool:
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO film (id_tmdb, title) VALUES (%s, %s) RETURNING id",
                    (id_tmdb, title)
                )
                new_id = cursor.fetchone()
                return new_id is not None

    def delete_movie(self, id_local: int) -> bool:
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM film WHERE id = %s RETURNING id", (id_local,))
                deleted_id = cursor.fetchone()
                return deleted_id is not None




