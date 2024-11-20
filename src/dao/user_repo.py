from typing import Optional

from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.Model.User import User


class UserRepo:
    """
    Cette méthode permet de récupérer un utilisateur par ID ou pseudo, d'ajouter de nouveaux utilisateurs, de mettre à jour leur pseudo, mot de passe ou statut d'éclaireur. 
    """

    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Cette méthode permet de récupèrer un utilisateur à partir de son identifiant.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur à récupérer.

        Retourne:
        ---------
        Optional[User]
            Un objet User si l'utilisateur est trouvé, sinon None.
        """
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"user_id": user_id})
                raw_user = cursor.fetchone()
        
        if raw_user is None:
            return None

        return User(**raw_user)

    def get_by_username(self, username: str) -> Optional[User]:

        """
        Cette méthode permet de récupèrer un utilisateur à partir de son pseudo.

        Paramètres:
        -----------
        username : str
            Le pseudo de l'utilisateur à récupérer.

        Retourne:
        ---------
        Optional[User]
            Un objet User si l'utilisateur est trouvé, sinon None.
        """

        query = "SELECT * FROM users WHERE username = %(username)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"username": username})
                raw_user = cursor.fetchone()

        if raw_user is None:
            return None
        return User(**raw_user)


    def insert_into_db(self, username: str, salt: str, hashed_password: str) -> User:
        """
        Cette méthode permet d'insèrer un nouvel utilisateur avec un pseudo, un sel et un mot de passe haché.

        Paramètres:
        -----------
        username : str
            Le pseudo de l'utilisateur à récupérer.

        salt : str
            Le sel (salt) utilisé pour hacher le mot de passe

        hashed_password : str
            Le mot de passe haché de l'utilisateur.

        Retourne:
        ---------
        User
            Un objet User représentant l'utilisateur créé dans la base de données.
        """
        query = """
        INSERT INTO users (id, username, salt, password)
        VALUES (DEFAULT, %(username)s, %(salt)s, %(password)s)
        RETURNING *;
        """
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    {"username": username, "salt": salt, "password": hashed_password}
                )
                raw_created_user = cursor.fetchone()
        if raw_created_user:
            return User(**raw_created_user)
        return None

    def update_pseudo(self, user_id: int, new_pseudo: str) -> bool:

        """
        Cette méthode permet de mettre à jour le pseudo d'un utilisateur dans la base de données.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur dont on souhaite changer le pseudo.
        
        new_pseudo : str:
            Le nouveau pseudo de l'utilisateur.

        Retourne:
        ---------
        Bool
            True si le pseudo a été mis à jour avec succès, sinon False.
        """
        query = "UPDATE users SET username = %(new_pseudo)s WHERE id = %(user_id)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"new_pseudo":new_pseudo, "user_id" :user_id}) 
                return cursor.rowcount > 0  # True si la mise à jour a réussi

    def update_password(self, user_id: int, hashed_password: str) -> bool:

        """
        Cette méthode permet de mettre à jour le mot de passe haché d'un utilisateur dans la base de données.
        
        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur dont on souhaite changer le pseudo.
        
        hashed_password : str:
            Le nouveau mot de passe haché de l'utilisateur.

        Retourne:
        ---------
        Bool
            True si le mot de passe a été mis à jour avec succès, sinon False.
        """

        query = "UPDATE users SET hashed_password = %(hashed_password)s WHERE id = %(user_id)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"hashed_password": hashed_password, "user_id" :user_id})
                return cursor.rowcount > 0

    def update_status(self, user_id: int, is_scout: bool) -> bool:

        """
        Cette méthode permet de mettre à jour le statut d'éclaireur (is_scout) d'un utilisateur dans la base de données.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur dont on souhaite changer le pseudo.
        
        is_scout :bool
             Le nouveau statut de l'utilisateur.

        Retourne:
        ---------
        Bool
            True si le statut de l'utilisateur a été mis à jour avec succès, sinon False.
        """

        query = "UPDATE users SET is_scout = %(is_scout)s WHERE id = %(user_id)s"
        with self.db_connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"is_scout": is_scout, "user_id" :user_id})
                return cursor.rowcount > 0

    def delete_by_id(self, user_id: int) -> bool:
        """
        Cette méthode permet de supprimer un utilisateur de la base de données par son identifiant.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur à supprimer.

        Retourne:
        ---------
        bool
            True si la suppression a été effectuée avec succès, sinon False.
        """
        user=self.get_by_id(user_id)
        if not user:
            return False
        query = "DELETE FROM users WHERE id = %(user_id)s"
        with self.db_connection.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, {"user_id": user_id})
                return cursor.rowcount > 0  




