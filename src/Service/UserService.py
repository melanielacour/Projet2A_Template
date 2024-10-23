from typing import List


class UserService:

    def __init__(self, user_dao, film_dao, review_dao):
        """
        Initialise le service avec les objets DAO (UserDAO, FilmDAO, ReviewDAO)
        pour interagir avec les données des utilisateurs, des films et des critiques.
        
        Paramètres:
        -----------
        user_dao : UserDAO
            Objet pour interagir avec les données des utilisateurs.
        film_dao : FilmDAO
            Objet pour interagir avec les données des films.
        review_dao : ReviewDAO
            Objet pour interagir avec les critiques des films.
        """
        self.user_dao = user_dao
        self.film_dao = film_dao
        self.review_dao = review_dao

    def log_in(self, username: str, password: str) -> None:
        """
        Permet à un utilisateur de se connecter avec un nom d'utilisateur et un mot de passe.
        
        Paramètres:
        -----------
        username : str
            Le nom d'utilisateur de l'utilisateur.
        password : str
            Le mot de passe de l'utilisateur.
        
        Retourne:
        ---------
        None
        
        Lève:
        -----
        ValueError:
            Si les identifiants sont incorrects ou que l'utilisateur n'existe pas.
        """
        user = self.user_dao.get_user_by_username(username)
    
        # Si l'utilisateur n'existe pas ou si le mot de passe ne correspond pas
        if not user or not self.user_dao.verify_password(user, password):
            raise ValueError("Nom d'utilisateur ou mot de passe incorrect")
            

    def get_scouts(self, user_id: int) -> List['Scout']:
        """
        Récupère la liste des éclaireurs (scouts) d'un utilisateur.
        
        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur.

        Retourne:
        ---------
        List[Scout]
            Liste des éclaireurs de l'utilisateur.
        """
        return self.user_dao.get_scouts(user_id)

    def get_seen_films(self, user_id: int) -> List['Film']:
        """
        Récupère la liste des films déjà vus par l'utilisateur.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur.

        Retourne:
        ---------
        List[Film]
            Liste des films vus par l'utilisateur.
        """
        return self.film_dao.get_seen_films(user_id)

    def get_to_watch_films(self, user_id: int) -> List['Film']:
        """
        Récupère la liste des films que l'utilisateur souhaite voir.

        Paramètres:
        -----------
        user_id : int
            L'identifiant de l'utilisateur.

        Retourne:
        ---------
        List[Film]
            Liste des films que l'utilisateur veut voir.
        """
        return self.film_dao.get_to_watch_films(user_id)

    def get_review(self, id_film: int, n: int) -> List['Review']:
        """
        Récupère les critiques d’un film.

        Paramètres:
        -----------
        id_film : int
            L'identifiant du film dont on souhaite récupérer les critiques.
        n : int
            Le nombre maximum de critiques à récupérer.

        Retourne:
        ---------
        List[Review]
            Liste des critiques du film.
        """
        return self.review_dao.get_reviews(id_film, n)

