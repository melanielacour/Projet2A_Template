import os
import time

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError  # Correction ici

from src.Model.JWTResponse import JWTResponse


class JwtService:
    """
    Gestionnaire pour le cryptage et la validation des JWT
    """

    def __init__(self, secret: str = "", algorithm: str = "HS256"):
        if secret == "":
            self.secret = os.environ["JWT_SECRET"]
        else:
            self.secret = secret
        self.algorithm = algorithm

    def encode_jwt(self, user_id: int) -> JWTResponse:
        """
        Crée un jeton avec une durée d'expiration de 10 minutes
        """
        payload = {"user_id": user_id, "expiry_timestamp": time.time() + 600}
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)

        return JWTResponse(access_token=token)

    def decode_jwt(self, token: str) -> dict:
        """
        Déchiffre un jeton d'authentification
        """
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def validate_user_jwt(self, token: str) -> str:
        """
        Renvoie l'identifiant de l'utilisateur authentifié par le JWT
        Lance en cas de JWT invalide ou expiré
        """
        decoded_jwt = self.decode_jwt(token)
        if decoded_jwt["expiry_timestamp"] < time.time():
            raise ExpiredSignatureError("Expired JWT")
        return decoded_jwt["user_id"]
