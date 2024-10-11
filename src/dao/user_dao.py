from typing import List
from utils.singleton import Singleton

from dao.db_connection import DBConnection
from dao.attack_dao import AttackDao

request = (
            f"SELECT *                                                               "
            f"  FROM users                                                    "
        )

with DBConnection().connection as connection:
    with connection.cursor() as cursor:
        cursor.execute(request)
        res = cursor.fetchall()