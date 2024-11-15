from pydantic import ValidationError
from src.Model.APIUser import APIUser  

def test_apiuser_initialization():
    """Test de l'initialisation d'un objet APIUser valide."""
    user = APIUser(id=1, username="testuser")
    assert user.id == 1
    assert user.username == "testuser"

def test_apiuser_invalid_id():
    """Test pour vérifier qu'une erreur est levée avec un ID invalide."""
    try:
        APIUser(id="invalid_id", username="testuser")  # ID invalide (doit être un int).
    except ValidationError as e:
        assert "id" in str(e)

def test_apiuser_invalid_username():
    """Test pour vérifier qu'une erreur est levée avec un nom d'utilisateur invalide."""
    try:
        APIUser(id=1, username=123)  # username invalide (doit être une str).
    except ValidationError as e:
        assert "username" in str(e)
