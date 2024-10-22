import hashlib
import secrets
from typing import Optional

from src.dao.UserRepo import UserRepo
from src.Model.Film import Film
from src.Model.User import User


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """
    Hache le mot de passe avec un sel optionnel en utilisant SHA-256.
    Si aucun sel n'est fourni, un nouveau sel est créé.
    """
    if salt is None:
        salt = create_salt()
    hashed_password = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed_password}"

def create_salt() -> str:
    """
    Génère un sel aléatoire sécurisé sur le plan cryptographique.
    """
    return secrets.token_hex(128)  

def check_password_strength(password: str):
    """
    Vérifie la force du mot de passe.
    Lève une exception si le mot de passe ne respecte pas les critères.
    """
    if len(password) < 8:
        raise ValueError("Password length must be at least 8 characters")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain at least one digit")

def validate_pseudo_password(pseudo: str, password: str, user_repo: UserRepo) -> User:
    """
    Valide le nom d'utilisateur et le mot de passe.
    Lève une exception si la validation échoue.
    """
    user_with_pseudo: Optional[User] = user_repo.get_by_pseudo(pseudo=pseudo)

    if not user_with_pseudo:
        raise Exception(f"User with pseudo {pseudo} not found")
    
    salt_stored = user_with_pseudo.password[:256]  # Longueur du sel (256 hex characters = 128 bytes)
    hashed_password_stored = user_with_pseudo.password[256:] 
    hashed_password = hash_password(password, salt_stored)[256:] 
    
    if hashed_password != hashed_password_stored:
        raise Exception("Incorrect password")

    return user_with_pseudo
