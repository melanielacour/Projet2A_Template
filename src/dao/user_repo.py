from typing import Optional
from src.Model.User import User
from src.dao.db_connection import DBConnection
from dotenv import load_dotenv

class UserRepo:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def get_by_id(self, user_id: int) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"user_id": user_id})
                raw_user = cursor.fetchone()
        
        if raw_user is None:
            return None

        return User(**raw_user)

    def get_by_username(self, username: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE username = %(username)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"username": username})
                raw_user = cursor.fetchone()

        if raw_user is None:
            return None
        return User(**raw_user)

    def insert_into_db(self, username: str, salt: str, hashed_password: str) -> User:
        query = """
        INSERT INTO users (id, username, salt, password)
        VALUES (DEFAULT, %(username)s, %(salt)s, %(password)s)
        RETURNING *;
        """
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    {"username": username, "salt": salt, "password": hashed_password}
                )
                raw_created_user = cursor.fetchone()

        return User(**raw_created_user)

    def update_pseudo(self, user_id: int, new_pseudo: str) -> bool:
        query = "UPDATE users SET username = %(new_pseudo)s WHERE id = %(user_id)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"new_pseudo":new_pseudo, "user_id" :user_id}) 
                return cursor.rowcount > 0  # True si la mise à jour a réussi

    def update_password(self, user_id: int, hashed_password: str) -> bool:
        query = "UPDATE users SET hashed_password = %(hashed_password)s WHERE id = %(user_id)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"hashed_password": hashed_password, "user_id" :user_id})
                return cursor.rowcount > 0

    def update_status(self, user_id: int, is_scout: bool) -> bool:
        query = "UPDATE users SET is_scout = %(is_scout)s WHERE id = %(user_id)s"
        with self.db_connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"is_scout": is_scout, "user_id" :user_id})
                return cursor.rowcount > 0


