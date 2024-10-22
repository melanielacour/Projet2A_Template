import os
import sys

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

from src.utils.singleton import Singleton


<<<<<<< HEAD:src/dao/DBConnector.py
class DBConnector(metaclass=Singleton):
=======
class DBConnection(metaclass=Singleton):
>>>>>>> 718e5441b4ed547c53f39a7138cfb0e56d2bf412:src/dao/db_connection.py
    """
    Une classe technique pour se connecter avec la base de données
    """
    def __init__(self):
        dotenv.load_dotenv(override=True)
        # Ouvrir la connexion grâce au .env
        self.__connection = psycopg2.connect(
            host=os.environ["HOST"],
            port=os.environ["PORT"],
            database=os.environ["DATABASE"],
            user=os.environ["USER"],
            password=os.environ["PASSWORD"],
            cursor_factory=RealDictCursor,
        )

    @property
    def connection(self):
        """
        Retourne la connexion ouverte
        """
        return self.__connection
