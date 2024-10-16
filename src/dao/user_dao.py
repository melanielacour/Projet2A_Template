from typing import List
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.singleton import Singleton

from dao.db_connection import DBConnection
from Model.user_simple import UserSimple

class UserDao(metaclass=Singleton):
    def get_all_user(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                   "
                    "FROM projet_2a.users;     "
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
        return liste_user



  
