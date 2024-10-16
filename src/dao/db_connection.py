import os

import dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.singleton import Singleton


class DBConnection(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self):
        dotenv.load_dotenv(override=True)
        # Open the connection.
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
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection