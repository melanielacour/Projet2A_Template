class User:
    """
    Classe qui représente un utilisateur dans PopcornCritic.

    Attributs:
    ----------
    id_user : int
        L'identifiant de l'utilisateur (unique).
    pseudo : str
        Le pseudo de l'utilisateur.
    password : str
        Le mot de passe de l'utilisateur.
    seen : List[Film]
        La liste des films que l'utilisateur a déjà vus.
    to_watch : List[Film]
        Une liste des films que l'utilisateur souhaite voir.
    scouts_list : List[Scout]
        Une liste d'éclaireurs que l'utilisateur suit.

    Méthodes:
    ---------
    add_seen(film: Film):
        Ajoute un film à la liste des films vus par l'utilisateur.

    add_to_watch(film: Film):
        Ajoute un film à la liste des films à regarder.

    add_scout(scout: Scout):
        Ajoute un éclaireur à la liste des éclaireurs suivis par l'utilisateur.

    """

    def __init__(self, id_user: int, pseudo: str, password: str,
                 seen : List[Film], to_watch : List[Film],
                 scouts_list = []):
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


    def add_to_watch(self, film: Film):
        """
        Ajoute un film à la liste des films à voir par l'utilisateur.

        Paramètres:
        -----------
        film : Film
            Le film à ajouter à la liste des films à voir.
        """
        self.to_watch.append(film)

    def add_scout(self, scout: Scout):
        """
        Ajoute un éclaireur à la liste des éclaireurs suivis par l'utilisateur.

        Paramètres:
        -----------
        scout : Scout
            L'éclaireur à ajouter à la liste des éclaireurs suivis.
        """
        self.scouts_list.append(scout)
