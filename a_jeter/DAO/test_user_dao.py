import pytest
from unittest.mock import MagicMock
from src.dao.user_repo import UserRepo
from src.dao.db_connection import DBConnection
from src.Model.User import User  # Assurez-vous que la classe User est importée correctement

@pytest.fixture
def db_connection_mock(mocker):
    # Mock the DBConnection class
    mock_db_connection = mocker.patch('src.dao.db_connection.DBConnection', autospec=True)
    
    # Create a mock connection and cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    
    # Set up the return values for the connection and cursor
    mock_db_connection.return_value.connection.return_value.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Initialize fetchone to return a dictionary
    mock_cursor.fetchone.return_value = {
        "id": 1,
        "username": "testuser",
        "salt": "salt",
        "password": "hashed_password"
    }
    
    return mock_db_connection

@pytest.fixture
def user_repo(db_connection_mock):
    return UserRepo(db_connection_mock)

def test_get_by_id(user_repo, db_connection_mock):
    # Arrange
    user_id = 1
    
    # Act
    user = user_repo.get_by_id(user_id)

    # Assert
    assert user is not None
    assert user.id == 1  # Check if the id matches
    assert user.username == "testuser"  # Check if the username matches
    assert user.salt == "salt"  # Check if the salt matches
    assert user.password == "hashed_password"  # Check if the password matches

def test_get_by_username(user_repo, db_connection_mock):
    # Arrange
    username = "testuser"
    mock_user = {"id": 1, "username": "testuser", "salt": "salt", "password": "hashed_password"}
    db_connection_mock.connection.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = mock_user

    # Act
    user = user_repo.get_by_username(username)

    # Assert
    assert user is not None
    assert isinstance(user, User)
    assert user.username == mock_user["username"]

def test_insert_into_db(user_repo, db_connection_mock):
    # Arrange
    new_username = "newuser"
    salt = "salt"
    hashed_password = "hashed_password"
    mock_created_user = {"id": 2, "username": new_username, "salt": salt, "password": hashed_password}
    db_connection_mock.connection.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = mock_created_user

    # Act
    user = user_repo.insert_into_db(new_username, salt, hashed_password)

    # Assert
    assert user is not None
    assert isinstance(user, User)
    assert user.id == mock_created_user["id"]
    assert user.username == mock_created_user["username"]

def test_get_by_id_not_found(user_repo, db_connection_mock):
    # Arrange
    user_id = 999
    db_connection_mock.connection.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = None

    # Act
    user = user_repo.get_by_id(user_id)

    # Assert
    assert user is None

def test_get_by_username_not_found(user_repo, db_connection_mock):
    # Arrange
    username = "unknownuser"
    db_connection_mock.connection.return_value.__enter__.return_value.cursor.return_value.fetchone.return_value = None

    # Act
    user = user_repo.get_by_username(username)

    # Assert
    assert user is None
