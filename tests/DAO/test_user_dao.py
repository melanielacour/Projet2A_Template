import pytest
from unittest import mock
from src.dao.user_dao import UserDao
from src.Model.user_simple import UserSimple

# Fixture pour simuler la connexion à la base de données
@pytest.fixture
def mock_db_connection(mocker):
    # Mock de la connexion DB
    mock_connection = mocker.patch('src.dao.db_connection.DBConnection')
    mock_cursor = mock.Mock()
    
    # Mock de la méthode cursor() pour retourner un mock du curseur
    mock_connection().connection.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_cursor

def test_create_user(mock_db_connection, mocker):
    # Création de l'objet UserDao
    user_dao = UserDao()

    # Mock de la méthode get_user_by_pseudo pour retourner None (pas d'utilisateur existant)
    mocker.patch.object(UserDao, 'get_user_by_pseudo', return_value=None)

    # Mock de l'insertion pour ne pas interagir avec la base de données réelle
    mock_db_connection.execute.return_value = None
    mock_db_connection.fetchone.return_value = {"id_users": 1}  # Simuler un ID retourné après insertion

    # Tester la création d'un utilisateur avec un pseudo unique
    new_user = user_dao.create_user("new_user4", is_scout=True, pswd="pass123")


    assert new_user is True


def test_create_user_with_duplicate_pseudo(mock_db_connection):
    user_dao = UserDao()
    
    # Tester la création avec un pseudo déjà existant
    with pytest.raises(ValueError, match="Nom d'utilisateur non disponible"):
        user_dao.create_user("john_doe", is_scout=False, pswd="password123")
