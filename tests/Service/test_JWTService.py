import os
import time
import jwt
import pytest
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.Model.JWTResponse import JWTResponse
from src.Service.JWTService import JwtService

# Utilisez une clé secrète pour les tests
TEST_SECRET = "test_secret"
TEST_ALGORITHM = "HS256"

@pytest.fixture
def jwt_service():
    """Fixture pour créer une instance de JwtService pour les tests."""
    return JwtService(secret=TEST_SECRET, algorithm=TEST_ALGORITHM)

def test_encode_jwt_creates_valid_token(jwt_service):
    """Test pour vérifier que encode_jwt crée un token JWT valide."""
    user_id = 1
    response = jwt_service.encode_jwt(user_id)
    assert isinstance(response, JWTResponse)
    assert response.access_token is not None

    # Vérification du contenu du token
    decoded_token = jwt.decode(response.access_token, TEST_SECRET, algorithms=[TEST_ALGORITHM])
    assert decoded_token["user_id"] == user_id
    assert "expiry_timestamp" in decoded_token
    assert decoded_token["expiry_timestamp"] > time.time()

def test_decode_jwt_returns_correct_payload(jwt_service):
    """Test pour vérifier que decode_jwt retourne le bon payload."""
    user_id = 1
    response = jwt_service.encode_jwt(user_id)
    decoded_payload = jwt_service.decode_jwt(response.access_token)

    assert decoded_payload["user_id"] == user_id
    assert "expiry_timestamp" in decoded_payload

def test_decode_jwt_invalid_token(jwt_service):
    """Test pour vérifier que decode_jwt lève une erreur pour un token invalide."""
    with pytest.raises(InvalidTokenError):
        jwt_service.decode_jwt("invalid_token")

def test_validate_user_jwt_valid_token(jwt_service):
    """Test pour vérifier que validate_user_jwt retourne l'ID utilisateur pour un token valide."""
    user_id = 1
    response = jwt_service.encode_jwt(user_id)
    validated_user_id = jwt_service.validate_user_jwt(response.access_token)
    
    assert validated_user_id == user_id

import time
import pytest
from jwt.exceptions import ExpiredSignatureError

def test_validate_user_jwt_expired_token(jwt_service, monkeypatch):
    """Test pour vérifier que validate_user_jwt lève une ExpiredSignatureError pour un token expiré."""
    user_id = 1

    # Fixer une valeur de temps de départ
    fixed_time = time.time()
    
    # Mock de time.time pour renvoyer une valeur fixe
    monkeypatch.setattr(time, "time", lambda: fixed_time)
    
    # Créer le jeton (token) en utilisant le temps fixe
    response = jwt_service.encode_jwt(user_id)
    
    # Avancer le temps pour simuler un token expiré
    monkeypatch.setattr(time, "time", lambda: fixed_time + 601)  # Temps actuel + 10 min + 1 sec

    # Vérifier que l'expiration du jeton déclenche ExpiredSignatureError
    with pytest.raises(ExpiredSignatureError):
        jwt_service.validate_user_jwt(response.access_token)


def test_validate_user_jwt_invalid_token(jwt_service):
    """Test pour vérifier que validate_user_jwt lève InvalidTokenError pour un token incorrect."""
    with pytest.raises(InvalidTokenError):
        jwt_service.validate_user_jwt("invalid_token")
