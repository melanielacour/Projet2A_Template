class UserDAO:
    """
    Classe qui gère le lien entre l'application et la table des films dans
    la base de données.

    Méthodes:
    ---------
    get_user(id_user : int) User
        Permet de récupérer les informations d'un utilisateur

    add_(User) : None
        ajouter un utilisateur à la table User de la bdd

    delete_user(user_id: int) : None
        supprimer un utilisateur de la table User de la bdd

    get_followers_of_scout(scout_id: int) : List[User

    """

    def __init__(self, id_user: int, pseudo: str, password: str,
                 seen: list[Film], to_watch: list[Film],
                 scouts_list=[]):
        """
        Initialise un nouvel utilisateur.

        Paramètres:
        -----------
        id_user : int
            L'identifiant unique de l'utilisateur.
        pseudo : str
            Le pseudo de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.
        """
        self.id_user = id_user
        self.pseudo = pseudo
        self.password = password
        self.seen = seen
        self.to_watch = to_watch
        self.scouts_list = scouts_list

    def add_seen(self, film: 'Film'):
        """
        Ajoute un film à la liste des films vus par l'utilisateur.

        Paramètres:
        -----------
        film : Film
            Le film à ajouter à la liste des films vus.
        """
        self.seen.append(film)
