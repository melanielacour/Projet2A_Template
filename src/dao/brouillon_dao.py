from db_connection import DBConnection
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()


db_connection = DBConnection()

# Requête SQL pour supprimer la table si elle existe avec cascade, puis la créer
create_table_query = """
DROP TABLE IF EXISTS projet_2a.users CASCADE;

CREATE TABLE projet_2a.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    salt VARCHAR(32) NOT NULL,
    password VARCHAR(255) NOT NULL
);
"""

# Exécution de la requête
with db_connection.connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
        connection.commit()  # Valider les modifications
