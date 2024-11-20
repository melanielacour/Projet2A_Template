import os
import pytest
from unittest.mock import MagicMock, patch
from src.Service.UserService import UserService

# Assurez-vous que la variable d'environnement JWT_SECRET est définie pour les tests
os.environ["JWT_SECRET"] = "test_secret"

@pytest.fixture
def user_service():
    """Fixture pour initialiser UserService avec des mocks."""
    service = UserService()
    service.user_repo = MagicMock()
    service.password_service = MagicMock()
    service.jwt_service = MagicMock()
    return service

def test_register_user_success(user_service):
    """Test pour l'inscription réussie d'un utilisateur."""
    pseudo = "testuser"
    password = "StrongPassword123"
    
    # Configurer le mock pour que l'utilisateur n'existe pas encore
    user_service.user_repo.get_by_username.return_value = None
    user_service.password_service.check_password_strength.return_value = None
    user_service.password_service.hash_password.return_value = "hashed_password"
    user_service.user_repo.create_user.return_value = True

    # Exécuter la méthode
    result = user_service.register_user(pseudo, password)

    # Vérifications
    assert result == "Vous êtes bien inscrit !"
    user_service.user_repo.get_by_username.assert_called_once_with(pseudo)
    user_service.password_service.check_password_strength.assert_called_once_with(password)
    user_service.user_repo.create_user.assert_called_once_with(username=pseudo, is_scout=False, password="hashed_password")

def test_register_user_existing_username(user_service):
    """Test pour l'inscription avec un identifiant déjà utilisé."""
    pseudo = "testuser"
    password = "StrongPassword123"

    # Configurer le mock pour que l'utilisateur existe déjà
    user_service.user_repo.get_by_username.return_value = True

    # Exécuter la méthode et vérifier l'exception
    with pytest.raises(ValueError, match="Cet identifiant est déjà utilisé."):
        user_service.register_user(pseudo, password)

def test_log_in_success(user_service):
    """Test pour la connexion réussie d'un utilisateur."""
    pseudo = "testuser"
    password = "StrongPassword123"
    mock_user = MagicMock()
    mock_user.id = 1
    user_service.user_repo.get_by_username.return_value = mock_user
    user_service.password_service.validate_password.return_value = True
    user_service.jwt_service.encode_jwt.return_value.access_token = "mock_jwt_token"

    # Exécuter la méthode
    result = user_service.log_in(pseudo, password)

    # Vérifications
    assert result == {"success": True, "token": "mock_jwt_token"}
    user_service.user_repo.get_by_username.assert_called_once_with(pseudo)
    user_service.password_service.validate_password.assert_called_once_with(pseudo, password)

def test_log_in_incorrect_username(user_service):
    """Test pour la connexion avec un identifiant incorrect."""
    pseudo = "unknown_user"
    password = "SomePassword"

    # Configurer le mock pour que l'utilisateur n'existe pas
    user_service.user_repo.get_by_username.return_value = None

    # Exécuter la méthode et vérifier l'exception
    with pytest.raises(ValueError, match="Identifiant incorrect."):
        user_service.log_in(pseudo, password)

def test_log_in_incorrect_password(user_service):
    """Test pour la connexion avec un mot de passe incorrect."""
    pseudo = "testuser"
    password = "WrongPassword"
    mock_user = MagicMock()
    mock_user.id = 1
    user_service.user_repo.get_by_username.return_value = mock_user
    user_service.password_service.validate_password.return_value = False

    # Exécuter la méthode et vérifier l'exception
    with pytest.raises(ValueError, match="Mot de passe incorrect."):
        user_service.log_in(pseudo="existing_user", password="WrongPassword123") 

    mock_user_dao.get_user_by_pseudo.assert_called_once_with("existing_user")
    mock_password_service.validate_password.assert_called_once_with("WrongPassword123", "ValidPassword123")














