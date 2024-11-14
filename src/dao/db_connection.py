import os
from typing import Literal, Optional, Union

import psycopg2
from psycopg2.extras import RealDictCursor


class DBConnection:
    """ 
    La classe permettant de gérer la connexion 
    avec la base de données locale PostgreSQL.

    Attributs :
    -----------
    
    """
    def __init__(self, config=None):
        if config is not None:
            self.host = config["host"]
            self.port = config["post"]
            self.database = config["database"]
            self.user = config["user"]
            self.password = config["password"]
            self.schema = config["schema"]
        else:
            self.host = os.environ["HOST"]
            self.port = os.environ["PORT"]
            self.database = os.environ["DATABASE"]
            self.user = os.environ["USER"]
            self.password = os.environ["PASSWORD"]
            self.schema = os.environ["SCHEMA"]

    def connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            password=self.password,
            schema=self.schema)
            