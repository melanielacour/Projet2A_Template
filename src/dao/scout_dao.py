from src.dao.db_connection import DBConnection
from src.Model.scout import Scout

class ScoutDao:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def become_scout(self, id_user):
        """Permet à un utilisateur de devenir éclaireur s'il a au moins 10 commentaires"""
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM projet_2a.review WHERE id_user = %(id_user)s;
                    """,
                    {"id_user": id_user}
                )
                count = cursor.fetchone()[0]

                if count >= 10:
                    cursor.execute(
                        """
                        INSERT INTO projet_2a.scouts (id_user)
                        VALUES (%(id_user)s)
                        ON CONFLICT (id_user) DO NOTHING;
                        """,
                        {"id_user": id_user}
                    )
                    return True
                return False

    def is_scout(self, id_user):
        """Vérifie si un utilisateur est éclaireur"""
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM projet_2a.scouts WHERE id_user = %(id_user)s;",
                    {"id_user": id_user}
                )
                return cursor.fetchone() is not None

    def get_all_scouts(self):
        """Récupère la liste de tous les éclaireurs"""
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM projet_2a.scouts;")
                rows = cursor.fetchall()

        return [Scout(row["id_user"]) for row in rows]
