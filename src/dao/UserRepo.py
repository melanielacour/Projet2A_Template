from typing import Optional

from src.dao.db_connection import DBConnection
from src.Model.User import User


class UserRepo:
    db_connection: DBConnection

    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def get_by_id(self, user_id: int) -> Optional[User]:
        raw_user = self.db_connection.sql_query("SELECT * from users WHERE id=%s", [user_id], "one")
        if raw_user is None:
            return None
        return User(**raw_user)

    def get_by_pseudo(self, pseudo: str) -> Optional[User]:
        raw_user = self.db_connection.sql_query("SELECT * from users WHERE pseudo=%s", [pseudo], "one")
        if raw_user is None:
            return None
        return User(**raw_user)

    def insert_into_db(self, pseudo: str, salt: str, hashed_password: str) -> User:
        raw_created_user = self.db_connection.sql_query(
            """
        INSERT INTO users (id, pseudo, salt, password)
        VALUES (DEFAULT, %(pseudo)s, %(salt)s, %(password)s)
        RETURNING *;
        """,
            {"pseudo": pseudo, "salt": salt, "password": hashed_password},
            "one",
        )

        return User(**raw_created_user)
