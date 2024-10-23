import hashlib
import re
import secrets
from typing import Optional

from src.dao.UserRepo import UserRepo
from src.Model.User import User


class PasswordService:
    def __init__(self):
        pass

    def hash_password(self, password: str, salt: Optional[str] = None) -> str:
        """
        Hache le mot de passe avec un sel optionnel en utilisant SHA-256.
        Si aucun sel n'est fourni, un nouveau sel est créé.
        """
        if salt is None:
            salt = self.create_salt()  # Appel à la méthode d'instance create_salt
        hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${hashed_password}"

    def create_salt(self) -> str:
        """
        Génère un sel aléatoire sécurisé sur le plan cryptographique.
        """
        return secrets.token_hex(128)

    def check_password_strength(self, password: str):
        """
        Vérifie la force du mot de passe.
        Lève une exception si le mot de passe ne respecte pas les critères.
        """
        if len(password) < 8:
            raise ValueError("Password length must be at least 8 characters")
        if not re.match(r'^[a-zA-Z0-9]+$', password):  # Vérifie l'absence de caractères spéciaux
            raise ValueError("Password must contain only letters and digits (no special characters)")
        if not any(c.islower() for c in password):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")

    def validate_pseudo_password(self, pseudo: str, password: str, user_repo: UserRepo) -> User:
        """
        Valide le nom d'utilisateur et le mot de passe.
        Lève une exception si la validation échoue.
        """
        user_with_pseudo: Optional[User] = user_repo.get_by_pseudo(pseudo=pseudo)

        if not user_with_pseudo:
            raise Exception(f"User with pseudo {pseudo} not found")

        self.check_password_strength(password)  # Appel à la méthode d'instance check_password_strength

        salt_stored = user_with_pseudo.password[:256]
        hashed_password_stored = user_with_pseudo.password[256:]
        hashed_password = self.hash_password(password, salt_stored)[256:]  # Appel à la méthode d'instance hash_password

        if hashed_password != hashed_password_stored:
            raise Exception("Incorrect password")

        return user_with_pseudo

    def validate_password(self, input_password: str, stored_password: str) -> bool:
        # Par exemple, si les mots de passe sont stockés sous forme de hachage, vous devrez les comparer après hachage
        return input_password == stored_password  # Remplacez par votre logique de validation
