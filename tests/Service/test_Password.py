import pytest
from src.Service.PasswordService import PasswordService

@pytest.fixture
def password_service():
    return PasswordService()


def test_create_salt(password_service):
    salt1 = password_service.create_salt()
    salt2 = password_service.create_salt()
    # Vérifie que le sel est de longueur 256 (128 hex chars)
    assert len(salt1) == 256
    # Vérifie que deux appels créent des sels différents
    assert salt1 != salt2


def test_hash_password_with_salt(password_service):
    password = "SecurePassword123"
    salt = "a" * 128  # Utilisation d'un sel fixe pour le test
    hashed_password = password_service.hash_password(password, salt)
    # Vérifie que le hachage est correctement formaté avec le sel en premier
    assert hashed_password.startswith(salt + "$")


def test_hash_password_without_salt(password_service):
    password = "SecurePassword123"
    # Génère un hachage sans fournir de sel
    hashed_password1 = password_service.hash_password(password)
    hashed_password2 = password_service.hash_password(password)
    # Les hachages doivent être différents car les sels sont générés aléatoirement
    assert hashed_password1 != hashed_password2


def test_check_password_strength_valid(password_service):
    password = "ValidPass123"
    # Ce mot de passe devrait passer toutes les vérifications
    assert password_service.check_password_strength(password) == password


def test_check_password_strength_length(password_service):
    password = "Short1"
    with pytest.raises(ValueError, match="Password length must be at least 8 characters"):
        password_service.check_password_strength(password)


def test_check_password_strength_special_chars(password_service):
    password = "Pass@123"
    with pytest.raises(ValueError, match="Password must contain only letters and digits"):
        password_service.check_password_strength(password)


def test_check_password_strength_lowercase(password_service):
    password = "PASSWORD123"
    with pytest.raises(ValueError, match="Password must contain at least one lowercase letter"):
        password_service.check_password_strength(password)


def test_check_password_strength_uppercase(password_service):
    password = "password123"
    with pytest.raises(ValueError, match="Password must contain at least one uppercase letter"):
        password_service.check_password_strength(password)


def test_check_password_strength_digit(password_service):
    password = "Password"
    with pytest.raises(ValueError, match="Password must contain at least one digit"):
        password_service.check_password_strength(password)


def test_validate_password(password_service):
    input_password = "SecurePassword123"
    stored_password = "SecurePassword123"
    # Vérifie que la validation passe avec des mots de passe identiques
    assert password_service.validate_password(input_password, stored_password)


def test_validate_password_incorrect(password_service):
    input_password = "SecurePassword123"
    stored_password = "WrongPassword123"
    # Vérifie que la validation échoue avec des mots de passe différents
    assert not password_service.validate_password(input_password, stored_password)
