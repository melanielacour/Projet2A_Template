import hashlib
import re
import secrets
from typing import Optional

from src.dao.UserRepo import UserRepo
from src.Model.User import User


class PasswordService:
    """
    Cette classe fournit les méthodes pour hacher les mots de passe, générer des sels,
    vérifier la force des mots de passe et valider les utilisateurs par rapport à leur
    pseudo et mot de passe.

    """

    def __init__(self):
        pass


    def hash_password(self, password: str, salt: Optional[str] = None) -> str:
        """
        Cette méthode prend un mot de passe et un sel et génère un hachage sécurisé du mot de passe à l'aide de l'algorithme SHA-256.

        Paramètres:
        -----------
        password : str
            Le mot de passe à hacher.
        salt : Optional[str]
            Le sel qu'on va utiliser pour le hachage.

        """
        # Si aucun sel n'est fourni, un nouveau sel est généré. 
        # Cela garantit que même si deux utilisateurs ont le même mot de passe, leurs hachages seront différents grâce à des sels uniques.
        if salt is None:
            salt = self.create_salt()
        hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${hashed_password}"


    def create_salt(self) -> str:
        """
        Cette méthode génére un sel aléatoire,avec une chaîne hexadécimale de 128 caractères.
        """
        return secrets.token_hex(128)



    def check_password_strength(self, password: str):
        """
        Cette méthode vérifie que le mot de passe respecte les critères tels que la longueur, la présence de lettres majuscules et minuscules, et de chiffres.
        Lève une exception si le mot de passe ne respecte pas les critères.
        
        Paramètres:
        -----------
        password : str
            Le mot de passe de l'utilisateur
        
        """
        # on verifie que le mot de passe a une longueur inférieur à 8 caractères. 
        if len(password) < 8:
            raise ValueError("Password length must be at least 8 characters")
        # on verifie que le mot de passe ne contient que des lettres et des chiffres, minuscules et chiffres
        if not re.match(r'^[a-zA-Z0-9]+$', password):  
            raise ValueError("Password must contain only letters and digits (no special characters)")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")
        else :
            return password



    def validate_pseudo_password(self, pseudo: str, password: str, user_repo: UserRepo) -> User:
        """
        Cette méthode valide un pseudo et un mot de passe en vérifiant que l'utilisateur existe et que le mot de passe fourni est correct.
        Si ce n'est pas le cas, on lève une exception si la validation échoue.

        Paramètres:
        -----------
        pseudo : str
            Le pseudo de l'utilisateur
        password : str
            Le mot de passe de l'utilisateur 
        user_repo : UserRepo
            Le dépôt d'utilisateurs utilisé pour récupérer les informations de l'utilisateur.

        Retourne:
        ---------
        User
            L'objet User correspondant au pseudo valide.
        """
        
        # on récupère l'utilisateur correspondant au pseudo depuis le dépôt d'utilisateurs.
        user_with_pseudo: Optional[User] = user_repo.get_by_pseudo(pseudo=pseudo)

        # une exception est levée pour éviter que des utilisateurs non enregistrés ne puissent tenter de se connecter.
        if not user_with_pseudo:
            raise Exception(f"User with pseudo {pseudo} not found")

        self.check_password_strength(password)  

        salt_stored = user_with_pseudo.password[:256]
        hashed_password_stored = user_with_pseudo.password[256:]
        hashed_password = self.hash_password(password, salt_stored)[256:]  

        if hashed_password != hashed_password_stored:
            raise Exception("Incorrect password")

        return user_with_pseudo



    def validate_password(self, input_password: str, stored_password: str) -> bool:
        """
        Cette méthode valide le mot de passe en le comparant avec le mot de passe stocké 
        Elle retourne True si les mots de passe correspondent, sinon False.
    
        Paramètres:
        -----------
        input_password : str
            Le mot de passe saisi par l'utilisateur.
        stored_password : str
            Le mot de passe stocké à valider.

        Retourne:
        ---------
        bool
            True si les mots de passe correspondent, sinon False.
        """
        return input_password == stored_password