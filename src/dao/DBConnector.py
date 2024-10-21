import os
import sys

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.singleton import Singleton


class DBConnector(metaclass=Singleton):
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



