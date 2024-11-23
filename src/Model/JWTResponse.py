from pydantic import BaseModel


class JWTResponse(BaseModel):
    """
    Représente la réponse contenant le token d'accès JWT.

    Attributs :
    -----------
    - access_token : str
        Le token d'accès JWT généré pour l'utilisateur après une
        authentification réussie.
    """
    access_token: str
