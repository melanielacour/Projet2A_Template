from pydantic import ValidationError
from src.Model.JWTResponse import JWTResponse 

def test_jwtresponse_initialization():
    """Test de l'initialisation d'un objet JWTResponse valide."""
    response = JWTResponse(access_token="valid_token")
    assert response.access_token == "valid_token"

def test_jwtresponse_invalid_access_token():
    """Test pour vérifier qu'une erreur est levée avec un access_token invalide."""
    try:
        JWTResponse(access_token=12345)  # `access_token` invalide (doit être une chaîne).
    except ValidationError as e:
        assert "access_token" in str(e)
