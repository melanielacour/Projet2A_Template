class User:
    """
    Cette classe représente un utilisateur aves ses attributs (identifiant,
    pseudo, mot de passe, statut d'éclaireur ou non). Elle est utilisée
    pour gérer les utilisateurs dans l'application.

    Attributs:
    ----------

    id: int
        L'identifiant de l'utilisateur
    username: int 
        Le pseudo de l'utilisateur
    salt :
    """
    def __init__(self, id: int, username: str, salt: str, password: str, is_scout:bool):
        self.id = id
        self.username = username
        self.salt = salt
        self.password = password
        self.is_scout=is_scout

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_scout='{self.is_scout}')>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        return False

