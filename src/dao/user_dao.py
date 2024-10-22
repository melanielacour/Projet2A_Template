import os
import sys
from typing import List
from src.dao.db_connection import DBConnection
from src.Model.user_simple import UserSimple
from src.utils.singleton import Singleton

from src.dao.db_connection import DBConnection
from src.Model.user_simple import UserSimple
from src.utils.singleton import Singleton


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class UserDao(metaclass=Singleton):
    def get_all_user_simple(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.users;"
                )
                res = cursor.fetchall()

        liste_user = []

        for row in res:
            user1 = UserSimple(
                id_user=row["id"],
                pseudo=row["pseudo"],
                is_scout=row["is_scout"],
                pswd=row["password"],
            )
            liste_user.append(user1)
        return {"users": liste_user}
    
    def get_user_by_id(self, id):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.users "
                    "WHERE id = %(id)s;            ",
                    {"id": id},
                )
                res = cursor.fetchone()

        if res:

            user1 = UserSimple(
                id_user=res["id"],
                pseudo=res["pseudo"],
                is_scout=res["is_scout"],
                pswd=res["passwords"],
            )
            return user1
        return None

    def get_user_by_pseudo(self, pseudo):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.users "
                    "WHERE pseudo = %(pseudo)s;    ",
                    {"pseudo": pseudo},
                )
                res = cursor.fetchone()

        if res:
            user1 = UserSimple(
                id_user=res["id"],
                pseudo=res["pseudo"],
                is_scout=res["is_scout"],
                pswd=res["password"],
            )
            return user1
        return None

    def create_user(self, pseudo, is_scout=False, pswd=None):
        # Vérification de l'unicité du pseudo
        user1 = self.get_user_by_pseudo(pseudo)
        if user1:
            raise ValueError("Nom d'utilisateur non disponible")
        
        # Si le pseudo est unique, création du nouvel utilisateur
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO projet_2a.users (pseudo, is_scout, password) "
                    "VALUES (%(pseudo)s, %(is_scout)s, %(pswd)s)              "
                    "RETURNING id;                                            ",
                    {
                        "pseudo": pseudo,
                        "is_scout": is_scout,
                        "pswd": pswd
                    },
                )
                res1 = cursor.fetchone()

        if res1:
            user1 = UserSimple(
                id_user=res1["id"],
                pseudo=pseudo,
                is_scout=is_scout,
                pswd=pswd
            )
            return True
        return False



