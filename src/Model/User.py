from typing import List

from src.Model.Film import Film


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
    is_scout : Bool
        False par défaut : si l'utilisateur est un éclaireur
    seen : list[Film]
        La liste des films que l'utilisateur a déjà vus.
    to_watch : list[Film]
        Une liste des films que l'utilisateur souhaite voir.
    scouts_list : list[Scout]
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
                 is_scout: bool, seen: list[Film], to_watch: list[Film],
                 scouts_list=[], salt: str = None):

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
        self.id_user= id_user
        self.pseudo = pseudo
        self.password = password
        self.is_scout = False
        self.seen = seen
        self.to_watch = to_watch
        self.scouts_list = scouts_list
        self.salt = salt

    def add_seen(self, film: 'Film'):
        """
        Ajoute un film à la liste des films vus par l'utilisateur.

        Paramètres:
        -----------
        film : Film
            Le film à ajouter à la liste des films vus.
        """
        self.seen.append(film)

    def add_to_watch(self, film: 'Film'):
        """
        Ajoute un film à la liste des films à voir par l'utilisateur.

        Paramètres:
        -----------
        film : Film
            Le film à ajouter à la liste des films à voir.

        Returns :
            None
        """
        self.to_watch.append(film)

    def add_scout(self, id_user: int):
        """
        Ajoute un éclaireur à la liste des éclaireurs suivis par l'utilisateur.

        Paramètres:
        -----------
        scout : Scout
            L'éclaireur à ajouter à la liste des éclaireurs suivis.

        Returns :

        """
        self.scouts_list.append(id_user)
