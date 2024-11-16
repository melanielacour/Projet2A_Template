class ValidationError(Exception):
    """Cette classe lève une exception pour les erreurs de validation."""
    pass


class User:
    """
    Cette classe représente un utilisateur avec ses attributs (identifiant,
    pseudo, mot de passe, statut d'éclaireur ou non). Elle est utilisée
    pour gérer les utilisateurs dans l'application. """

    def __init__(self, id: int, username: str, salt: str, password: str, is_scout: bool):

        """
        Cette méthode permet de mettre à jour le statut d'éclaireur (is_scout) d'un utilisateur dans la base de données.

        Parameters :
        -----------
        id : int 
            L'identifiant unique de l'utilisateur.
        username : str
            Le pseudo de l'utilisateur.
        salt : str
            Le sel utilisé pour le hachage du mot de passe.
        password : str
            e mot de passe de l'utilisateur.
        is_scout : bool
            Le statut de l'utilisateur, qui indique s'il est un éclaireur ou non.
        """

        # Vérification des types des attributs
        if not isinstance(id, int):
            raise ValidationError("id must be an integer")
        if not isinstance(username, str):
            raise ValidationError("username must be a string")
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
        """
        Cette méthode retourne une chaîne de caractères représentant l'objet User
        """

        return f"<User(id={self.id}, username='{self.username}', is_scout={self.is_scout})>"


    def __eq__(self, other):
        """
        Cette méthode permet de savoir si deux objets User représentent le même utilisateur en se basant uniquement sur leur identifiant.
        
        Parameters :
        -----------
        other : 
            Un autre objet à comparer avec l'objet actuel.
        """

        if isinstance(other, User):
            return self.id == other.id
        return False