import random
from unittest.mock import Mock

import pytest

from src.Model.User import User
from src.Service.UserService import (UserService, average_rate,
                                     get_review_by_title)


def test_register_user_success():
    # on teste le succès de l'inscription d'un nouvel utilisateur.
    mock_user_dao = Mock()
    mock_password_service = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=mock_password_service)

    mock_user_dao.get_user_by_pseudo.return_value = None  # L'utilisateur n'existe pas encore
    mock_password_service.validate_password.return_value = True  # Le mot de passe est valide
    mock_user_dao.create_user.return_value = True  # Création réussie de l'utilisateur

    result = user_service.register_user(pseudo="new_user", password="ValidPassword123", is_scout=False)

    assert result == "Vous êtes bien inscrit !"  # Vérifiez le message de succès
    mock_user_dao.get_user_by_pseudo.assert_called_once_with("new_user")
    mock_password_service.validate_password.assert_called_once_with("ValidPassword123")
    mock_user_dao.create_user.assert_called_once_with(pseudo="new_user", is_scout=False, pswd="ValidPassword123")



def test_register_user_existing_pseudo():
    # on teste l'inscription d'un utilisateur avec un pseudo déjà utilisé.
    mock_user_dao = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=Mock())

    # on a initié un utlisateur avec les caractéristiques suivantes : 
    mock_user_dao.get_user_by_pseudo.return_value = User(
        id_user=1,
        pseudo="existing_user",
        password="password",  
        is_scout=False,
        seen=[],  
        to_watch=[],  
        scouts_list=[] 
    )
    
    with pytest.raises(ValueError, match="Cet identifiant est déjà utilisé."):
        user_service.register_user(pseudo="existing_user", password="Password123", is_scout=False)

    mock_user_dao.get_user_by_pseudo.assert_called_once_with("existing_user")



def test_register_user_invalid_password():
    # on teste l'inscription avec un mot de passe invalide.
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
    
    mock_user_dao.get_user_by_pseudo.return_value = user  
    mock_password_service.validate_password.return_value = True 

    result = user_service.log_in(pseudo="existing_user", password="ValidPassword123")

    assert result is True
    mock_user_dao.get_user_by_pseudo.assert_called_once_with("existing_user")
    mock_password_service.validate_password.assert_called_once_with("ValidPassword123", "ValidPassword123")



def test_log_in_invalid_pseudo():
    mock_user_dao = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=Mock())

    mock_user_dao.get_user_by_pseudo.return_value = None

    with pytest.raises(ValueError, match="Identifiant incorrect."):
        user_service.log_in(pseudo="nonexistent_user", password="ValidPassword123")

    mock_user_dao.get_user_by_pseudo.assert_called_once_with("nonexistent_user")


def test_log_in_invalid_password():
    mock_user_dao = Mock()
    mock_password_service = Mock()
    user_service = UserService(user_dao=mock_user_dao, password_service=mock_password_service)

    # on a un utilisateur avec un mot de passe correct
    user = User(
        id_user=1,
        pseudo="existing_user",
        password="ValidPassword123",  # Assurez-vous que c'est 'password'
        is_scout=False,
        seen=[], 
        to_watch=[], 
        scouts_list=[]  
    )

    mock_user_dao.get_user_by_pseudo.return_value = user

    # Configurez le mock pour que validate_password retourne False pour le mot de passe incorrect
    mock_password_service.validate_password.return_value = False 

    with pytest.raises(ValueError, match="Mot de passe incorrect."):
        user_service.log_in(pseudo="existing_user", password="WrongPassword123") 

    mock_user_dao.get_user_by_pseudo.assert_called_once_with("existing_user")
    mock_password_service.validate_password.assert_called_once_with("WrongPassword123", "ValidPassword123")














# Simulation de la classe ReviewDao
class MockReviewDao:
    @staticmethod
    def get_all_review_by_title(title):
        if title == "Film A":
            return [
                {'id_user': 1, 'note': 8.0, 'comment': 'Super film!'},
                {'id_user': 2, 'note': 7.5, 'comment': 'Bien mais pas incroyable.'},
                {'id_user': 3, 'note': 9.0, 'comment': 'Un chef-d\'œuvre!'},
                {'id_user': 4, 'note': 6.0, 'comment': 'Moyen.'},
                {'id_user': 5, 'note': 7.0, 'comment': 'Pas mal.'},  # Utilisateur avec une note valide
                {'id_user': 6, 'note': 7.0, 'comment': 'Assez bon!'},  # Commentaire valide
            ]
        elif title == "Film B":
            return [
                {'id_user': 7, 'note': 5.5, 'comment': 'Pas terrible.'},
                {'id_user': 8, 'note': 6.5, 'comment': 'Assez bon.'},
                {'id_user': 9, 'note': 8.5, 'comment': 'J\'adore ce film!'},
            ]
        return []


def test_average_rate():
    # Test de la fonction average_rate
    assert average_rate("Film A") == "La note moyenne de 'Film A' est de 7.42."
    assert average_rate("Film B") == "La note moyenne de 'Film B' est de 6.83."
    assert average_rate("Film C") == "Aucune note disponible pour le film 'Film C'."
    print("Tous les tests de average_rate sont passés.")


def test_get_review_by_title():
    # Test de la fonction get_review_by_title
    result = get_review_by_title("Film A", 3)
    assert "Voici les notes et commentaires de" in result
    assert len(result.split(':')[1].strip(' "')) <= 3  # Vérifie que le nombre d'avis ne dépasse pas 3

    result_b = get_review_by_title("Film B", 2)
    assert "Voici les notes et commentaires de" in result_b
    assert len(result_b.split(':')[1].strip(' "')) <= 2  # Vérifie que le nombre d'avis ne dépasse pas 2

    result_c = get_review_by_title("Film C", 5)
    assert "Voici les notes et commentaires de" in result_c
    assert "0 utilisateurs" in result_c  # Vérifie que l'on reçoit 0 utilisateurs pour Film C

    print("Tous les tests de get_review_by_title sont passés.")