from src.dao.user_movies_dao import UserMovieDao
from src.Model.user_movie import UserMovie

class UserMovieService:
    def __init__(self, user_movie_dao: UserMovieDao):
        self.user_movie_dao = user_movie_dao

    def get_watchlist(self, id_user):
        """
        Récupère la liste des films que l'utilisateur souhaite regarder.
        """
        return self.user_movie_dao.get_movies_by_user(id_user, status="to_watch")

    def get_seenlist(self, id_user):
        """
        Récupère la liste des films que l'utilisateur a déjà regardés.
        """
        return self.user_movie_dao.get_movies_by_user(id_user, status="watched")

    def add_movie_to_watchlist(self, id_user, id_film):
        """
        Ajoute un film à la liste des films à regarder.
        """
        self.user_movie_dao.add_movie(id_user, id_film, status="to_watch")

    def add_movie_to_seenlist(self, id_user, id_film):
        """
        Ajoute un film à la liste des films vus.
        """
        self.user_movie_dao.add_movie(id_user, id_film, status="watched")

    def delete_movie_from_list(self, id_user, id_film, status):
        """
        Supprime un film de la liste des films à voir ou vus.
        """
        return self.user_movie_dao.delete_movie(id_user, id_film, status)

    def update_movie_status(self, id_user, id_film, new_status):
        """
        Modifie le statut d'un film (à voir ou déjà vu).
        """
        if new_status not in ["watched", "to_watch"]:
            raise ValueError("Statut invalide. Utilisez 'watched' ou 'to_watch'.")
        self.user_movie_dao.add_movie(id_user, id_film, new_status)
