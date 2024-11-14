class UserMovie:
    """
    Cette classe représente la relation entre un utilisateur et un film.

    Attributs:
    ----------
    id_user : int
        L'identifiant de l'utilisateur (unique).
    id_film : int
        L'identifiant du film dans la base de données (unique aussi).
    status : str
        Le statut de la relation entre l'utilisateur et le film.

    Méthodes:
    ---------
    __repr__(self) -> str
        Retourne une représentation en chaîne de caractères de UserMovie.
    """
    def __init__(self, id_user, id_film, status):
        """
        Initialise une nouvelle instance de UserMovie.

        Paramètres:
        -----------
        id_user : int
            L'identifiant de l'utilisateur.
        id_film : int
            L'identifiant du film dans la base de données.
        status : str
            Le statut de la relation entre l'utilisateur et le film.
        """
        self.id_user = id_user
        self.id_film = id_film
        self.status = status

    def __repr__(self):
        """ Retourne une représentation en chaîne de caractères de UserMovie"""
        return f"UserMovie(id_user={self.id_user}, id_film={self.id_film}, status='{self.status}')"
