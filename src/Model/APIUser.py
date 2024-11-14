from pydantic import BaseModel


class APIUser(BaseModel):
    """
    Cette classe représente un utilisateur dans notre API.
    Il a pour attribut son identifiant et son nom.

    Attributs:
    ----------

    id : int
        L'identifiant de l'utilisateur
    username : str
        Le nom de l'utilisateur
    """
    id: int
    username: str
