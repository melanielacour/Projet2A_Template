from unittest.mock import Mock

import pytest

from src.Model.User import User
from src.Service.UserService import UserService


def test_register_user_success():
    mock_user_dao = Mock()
    mock_password_service = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=mock_password_service)

    mock_user_dao.get_user_by_pseudo.return_value = None  # L'utilisateur n'existe pas encore
    mock_password_service.validate_password.return_value = True  # Le mot de passe est valide
    mock_user_dao.create_user.return_value = True  # Simulation de la création réussie de l'utilisateur

    result = user_service.register_user(pseudo="new_user", password="ValidPassword123", is_scout=False)

    assert result == "Vous êtes bien inscrit !"  # Vérifiez le message de succès
    mock_user_dao.get_user_by_pseudo.assert_called_once_with("new_user")
    mock_password_service.validate_password.assert_called_once_with("ValidPassword123")
    mock_user_dao.create_user.assert_called_once_with(pseudo="new_user", is_scout=False, pswd="ValidPassword123")



def test_register_user_existing_pseudo():
    mock_user_dao = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=Mock())

    # Créez un utilisateur avec tous les arguments nécessaires
    mock_user_dao.get_user_by_pseudo.return_value = User(
        id_user=1,
        pseudo="existing_user",
        password="password",  # Assurez-vous que c'est 'password' et pas 'pswd'
        is_scout=False,
        seen=[],  # Liste vide pour le test
        to_watch=[],  # Liste vide pour le test
        scouts_list=[]  # Liste vide pour le test
    )
    
    # Vérifiez si l'exception est levée
    with pytest.raises(ValueError, match="Cet identifiant est déjà utilisé."):
        user_service.register_user(pseudo="existing_user", password="Password123", is_scout=False)

    # Vérification que la méthode a été appelée avec le bon pseudo
    mock_user_dao.get_user_by_pseudo.assert_called_once_with("existing_user")





def test_register_user_invalid_password():
    mock_user_dao = Mock()
    mock_password_service = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=mock_password_service)

    mock_user_dao.get_user_by_pseudo.return_value = None  # L'utilisateur n'existe pas
    mock_password_service.validate_password.return_value = False  # Mot de passe non valide

    with pytest.raises(ValueError, match="Le mot de passe doit comporter au moins une majuscule, une minuscule et un chiffre."):
        user_service.register_user(pseudo="new_user", password="invalidpassword", is_scout=False)

    mock_password_service.validate_password.assert_called_once_with("invalidpassword")


def test_log_in_success():
    mock_user_dao = Mock()
    mock_password_service = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=mock_password_service)

    user = User(
        id_user=1,
        pseudo="existing_user",
        password="ValidPassword123",  # Utilisez 'password'
        is_scout=False,
        seen=[],  # Liste vide pour le test
        to_watch=[],  # Liste vide pour le test
        scouts_list=[]  # Liste vide pour le test
    )
    
    mock_user_dao.get_user_by_pseudo.return_value = user  # L'utilisateur existe
    mock_password_service.validate_password.return_value = True  # Simulation d'un mot de passe valide

    result = user_service.log_in(pseudo="existing_user", password="ValidPassword123")

    assert result is True
    mock_user_dao.get_user_by_pseudo.assert_called_once_with("existing_user")
    mock_password_service.validate_password.assert_called_once_with("ValidPassword123", "ValidPassword123")



def test_log_in_invalid_pseudo():
    mock_user_dao = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=Mock())

    mock_user_dao.get_user_by_pseudo.return_value = None  # L'utilisateur n'existe pas

    with pytest.raises(ValueError, match="Identifiant incorrect."):
        user_service.log_in(pseudo="nonexistent_user", password="ValidPassword123")

    mock_user_dao.get_user_by_pseudo.assert_called_once_with("nonexistent_user")


def test_log_in_invalid_password():
    mock_user_dao = Mock()
    mock_password_service = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=mock_password_service)

    # Créez un utilisateur avec le mot de passe correct
    user = User(
        id_user=1,
        pseudo="existing_user",
        password="ValidPassword123",  # Assurez-vous que c'est 'password'
        is_scout=False,
        seen=[],  # Liste vide pour le test
        to_watch=[],  # Liste vide pour le test
        scouts_list=[]  # Liste vide pour le test
    )

    mock_user_dao.get_user_by_pseudo.return_value = user  # L'utilisateur existe

    # Configurez le mock pour que validate_password retourne False pour le mot de passe incorrect
    mock_password_service.validate_password.return_value = False  # Simulez un mot de passe incorrect

    with pytest.raises(ValueError, match="Mot de passe incorrect."):
        user_service.log_in(pseudo="existing_user", password="WrongPassword123")  # Mot de passe incorrect

    mock_user_dao.get_user_by_pseudo.assert_called_once_with("existing_user")
    mock_password_service.validate_password.assert_called_once_with("WrongPassword123", "ValidPassword123")

