import pytest
from src.Model.User import User, ValidationError


def test_valid_user_creation():
    """Test de création d'un utilisateur valide."""
    user = User(id=1, username="JohnDoe", salt="random_salt", password="secure_pass", is_scout=True)
    assert user.id == 1
    assert user.username == "JohnDoe"
    assert user.salt == "random_salt"
    assert user.password == "secure_pass"
    assert user.is_scout is True


def test_invalid_id_type():
    """Test de levée d'une exception si id n'est pas un entier."""
    with pytest.raises(ValidationError, match="id must be an integer"):
        User(id="1", username="JohnDoe", salt="random_salt", password="secure_pass", is_scout=True)


def test_invalid_username_type():
    """Test de levée d'une exception si username n'est pas une chaîne."""
    with pytest.raises(ValidationError, match="username must be a string"):
        User(id=1, username=12345, salt="random_salt", password="secure_pass", is_scout=True)



def test_invalid_password_type():
    """Test de levée d'une exception si password n'est pas une chaîne."""
    with pytest.raises(ValidationError, match="password must be a string"):
        User(id=1, username="JohnDoe", salt="random_salt", password=12345, is_scout=True)


def test_invalid_is_scout_type():
    """Test de levée d'une exception si is_scout n'est pas un booléen."""
    with pytest.raises(ValidationError, match="is_scout must be a boolean"):
        User(id=1, username="JohnDoe", salt="random_salt", password="secure_pass", is_scout="True")


def test_equality_between_users():
    """Test de comparaison entre deux utilisateurs."""
    user1 = User(id=1, username="JohnDoe", salt="salt1", password="pass1", is_scout=False)
    user2 = User(id=1, username="JaneDoe", salt="salt2", password="pass2", is_scout=True)
    user3 = User(id=2, username="JohnDoe", salt="salt3", password="pass3", is_scout=False)

    assert user1 == user2  # Même id
    assert user1 != user3  # Id différents
