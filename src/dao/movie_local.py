
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
    def get_all_movie(self):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.film;"
                )