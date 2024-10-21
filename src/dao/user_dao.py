import os
import sys
from typing import List

from src.dao.db_connection import DBConnection
from src.Model.user_simple import UserSimple
from src.utils.singleton import Singleton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class UserDao(metaclass=Singleton):
    def get_all_user_simple(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                   "
                    "FROM projet_2a.users;      "
        )
        res = cursor.fetchall()

        liste_user = []

        for row in res:
            user1 = UserSimple(
                id_user=row["id"],
                pseudo=row["pseudo"],
                is_scout=row["is.scout"],
            )
            liste_user.append(user1)
        return {"users": liste_user}

    def get_user_by_id(self,id):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                   "
                    "FROM projet_2a.users;      "
                    "WHERE id_users=%(id)s      ",
                    {"id": id},
        )
        res = cursor.fetchone()

        if res:
            user1=UserSimple(
                id_user=row["id"],
                pseudo=row["pseudo"],
                is_scout=row["is.scout"],
            )
        return user1

    #def create_user(self, pseudo, is_scout=False):
