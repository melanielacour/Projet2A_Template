import os
import time

import jwt
from jwt.exceptions import ExpiredSignatureError  # Correction ici
from jwt.exceptions import InvalidTokenError

from src.Model.JWTResponse import JWTResponse


class JwtService:
    """
    Cette méthode gère la création, la déchiffrement et la validation de jetons JWT pour authentifier les utilisateurs de manière sécurisée.
    """

    def __init__(self, secret: str = "", algorithm: str = "HS256"):
        if secret == "":
            self.secret = os.environ["JWT_SECRET"]
        else:
            self.secret = secret
        self.algorithm = algorithm

    def encode_jwt(self, user_id: int) -> JWTResponse:
        """
        Cette méthode génère un nouveau JWT incluant son identifiant (user_id) et une date d'expiration fixée à 10 minutes.

        Paramètres:
        -----------
        user_id : int
            Identifiant de l'utilisateur
        
        Retourne:
        ---------
        JWTResponse

        """
        payload = {"user_id": user_id, "expiry_timestamp": time.time() + 600}
        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)

        return JWTResponse(access_token=token)

    def decode_jwt(self, token: str) -> dict:
        """
        Cette méthode permet de déchiffrer un jeton d'authentification

        Paramètres:
        -----------
        token : str
            Le JWT à décoder
        
        Retourne:
        ---------
        dict
            Dictionnaire contenant les données décryptées du jeton
        """
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])

    def validate_user_jwt(self, token: str) -> str:
        """
        Cette méthode renvoie l'identifiant de l'utilisateur authentifié par le JWT
        Lance en cas de JWT invalide ou expiré

         Paramètres:
        -----------
        token : str
            Le JWT à décoder
        
        Retourne:
        ---------
        str
           Une chaine contenant l'identifiant de l'utilisateur

        """
        decoded_jwt = self.decode_jwt(token)
        if decoded_jwt["expiry_timestamp"] < time.time():
            raise ExpiredSignatureError("Expired JWT")
        return decoded_jwt["user_id"]
