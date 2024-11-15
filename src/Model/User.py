class ValidationError(Exception):
    """Cette classe lève une exception pour les erreurs de validation."""
    pass


class User:
    """
    Cette classe représente un utilisateur avec ses attributs (identifiant,
    pseudo, mot de passe, statut d'éclaireur ou non). Elle est utilisée
    pour gérer les utilisateurs dans l'application.

    Attributs:
    ----------
    id: int
        L'identifiant de l'utilisateur.
    username: str
        Le pseudo de l'utilisateur.
    salt: str
        Le sel utilisé pour le hachage du mot de passe.
    password: str
        Le mot de passe de l'utilisateur.
    is_scout: bool
        Indique si l'utilisateur est un éclaireur ou non.
    """

    def __init__(self, id: int, username: str, salt: str, password: str, is_scout: bool):
        # Vérification des types des attributs
        if not isinstance(id, int):
            raise ValidationError("id must be an integer")
        if not isinstance(username, str):
            raise ValidationError("username must be a string")
        if not isinstance(salt, str):
            raise ValidationError("salt must be a string")
        if not isinstance(password, str):
            raise ValidationError("password must be a string")
        if not isinstance(is_scout, bool):
            raise ValidationError("is_scout must be a boolean")

        self.id = id
        self.username = username
        self.salt = salt
        self.password = password
        self.is_scout = is_scout

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', is_scout={self.is_scout})>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        return False