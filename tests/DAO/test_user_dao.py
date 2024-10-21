import pytest
from unittest.mock import MagicMock
from src.dao.user_dao import UserDao
from src.Model.user_simple import UserSimple


@pytest.fixture
def mock_db_connection(mocker):
    """
    Fixture pour simuler la connexion à la base de données.
    """
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    
    # Simuler le curseur de la base de données
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Simuler la méthode fetchall du curseur
    mock_cursor.fetchall.return_value = [
        {'id': 1, 'pseudo': 'john_doe', 'is_scout': True},
        {'id': 2, 'pseudo': 'jane_doe', 'is_scout': False},
    ]
    
    # Retourner la connexion simulée
    mocker.patch('src.dao.db_connection.DBConnection', return_value=mock_connection)
    return mock_connection


def test_create_user(mock_db_connection):
    user_dao = UserDao()
    
    # Tester la création d'un utilisateur avec un pseudo unique
    new_user = user_dao.create_user("new_user", is_scout=True, pswd="password123")
    
    assert new_user is not None
    assert new_user.pseudo == "new_user"
    assert new_user.is_scout is True
    assert new_user.pswd == "password123"


def test_create_user_with_duplicate_pseudo(mock_db_connection):
    user_dao = UserDao()
    
    # Tester la création avec un pseudo déjà existant
    with pytest.raises(ValueError, match="Nom d'utilisateur non disponible"):
        user_dao.create_user("john_doe", is_scout=False, pswd="password123")
