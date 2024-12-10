from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.dao.movie_local import MovieRepo
from src.dao.review_dao import ReviewDao
from src.Model.Review import Review

load_dotenv()


class ReviewService:
    """
    Service pour gérer les critiques des films.
    """

    def __init__(self, review_dao: ReviewDao):
        self.review_dao = review_dao

    def search_and_rate_movie_existing_movie(
        self, id_film, id_user, note, comment
    ):

        """
        Recherche un film, puis ajoute ou
        modifie une critique d'un utilisateur.

        Parameters:
            id_film (int): L'ID du film.
            id_user (int): L'ID de l'utilisateur.
            note (float): La note donnée au film.
            comment (str): Le commentaire de l'utilisateur.

        Returns:
            str: Un message indiquant si la critique a été ajoutée ou modifiée.
        """
        movie = MovieRepo(DBConnection()).get_movie_by_id_film(id_film)
        if not movie:
            raise ValueError("Identifiant de film incorrect")

        existing_review = self.review_dao.get_review_by_id_user_and_id_film(
            id_film, id_user
        )
        if existing_review:
            self.update_comment(
                id_film=id_film,
                id_user=id_user,
                comment=comment
                )
            self.update_note(id_film=id_film, id_user=id_user, note=note)
            return "Votre critique à été modifiée"
        else:
            new_review = Review(
                id_review=None,
                id_film=id_film,
                id_user=id_user,
                note=note,
                comment=comment,
            )
            return self.review_dao.add_review(new_review)

    def update_note(self, id_user, id_film, note):
        """
        Met à jour une critique existante avec une nouvelle note.

        Parameters:
            id_user (int): L'ID de l'utilisateur.
            id_film (int): L'ID du film.
            note (float): La nouvelle note à attribuer.

        Returns:
            bool: True si la mise à jour a réussi.
        """
        existing_review = self.review_dao.get_review_by_id_user_and_id_film(
            id_film, id_user
        )
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        existing_review.note = note
        return self.review_dao.update_review(existing_review)

    def update_comment(self, id_user, id_film, comment):
        """
        Met à jour une critique existante avec un nouveau commentaire.

        Parameters:
            id_user (int): L'ID de l'utilisateur.
            id_film (int): L'ID du film.
            comment (str): Le nouveau commentaire.

        Returns:
            bool: True si la mise à jour a réussi.
        """
        existing_review = self.review_dao.get_review_by_id_user_and_id_film(
            id_film, id_user
        )
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        existing_review.comment = comment
        return self.review_dao.update_review(existing_review)

    def delete_review(self, id_film, id_user):
        """
        Supprime une critique spécifique pour un film donné par un utilisateur.

        Parameters:
            id_film (int): L'ID du film.
            id_user (int): L'ID de l'utilisateur.

        Returns:
            bool: True si la suppression a réussi.
        """
        return self.review_dao.delete_review(id_user, id_film)

    def delete_note(self, id_film, id_user):
        """
        Supprime la note d'un film pour un utilisateur.

        Parameters:
            id_film (int): L'ID du film.
            id_user (int): L'ID de l'utilisateur.

        Returns:
            bool: True si la suppression a réussi.
        """
        existing_review = self.review_dao.get_review_by_id_user_and_id_film(
            id_film, id_user
        )
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        return self.delete_review(id_film=id_film, id_user=id_user)

    def delete_comment(self, id_film, id_user):
        """
        Supprime le commentaire d'un film pour un utilisateur.

        Parameters:
            id_film (int): L'ID du film.
            id_user (int): L'ID de l'utilisateur.

        Returns:
            bool: True si la suppression a réussi.
        """
        existing_review = self.review_dao.get_review_by_id_user_and_id_film(
            id_film, id_user
        )
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        if not existing_review.note:
            return self.delete_review(id_film=id_film, id_user=id_user)
        return self.update_comment(
            id_film=id_film,
            id_user=id_user,
            comment=None
            )

    def get_average_rating(self, id_film):
        """
        Calcule la note moyenne des utilisateurs pour un film donné.

        Parameters:
            id_film (int): L'ID du film.

        Returns:
            float: La note moyenne du film, ou 0 si aucune critique n'existe.
        """
        all_reviews = self.review_dao.get_all_review_by_id(id_film)
        if not all_reviews:
            return 0

        total_rating = sum(review.note for review in all_reviews)
        return total_rating / len(all_reviews)

    def search_and_rate_movie_by_idtmdb(
        self, id_tmdb, title, id_user, note, comment
    ):
        """
        Recherche un film par son ID TMDB, puis ajoute ou modifie une critique.

        Parameters:
            id_tmdb (int): L'ID TMDB du film.
            title (str): Le titre du film.
            id_user (int): L'ID de l'utilisateur.
            note (float): La note donnée au film.
            comment (str): Le commentaire de l'utilisateur.

        Returns:
            str: Un message indiquant si la critique a été ajoutée ou modifiée.
        """
        movie = MovieRepo(DBConnection()).get_movie_by_tmdb_id(id_tmdb)
        if not movie:
            movie2 = MovieRepo(DBConnection()).add_movie(
                id_tmdb=id_tmdb, title=title
                )
            movie = MovieRepo(DBConnection()).get_movie_by_tmdb_id(id_tmdb)
            if not movie2:
                raise ValueError(
                    "Échec de l'ajout du film dans la base données"
                    )
        return self.search_and_rate_movie_existing_movie(
            movie.id_local, id_user, note, comment
        )

    def get_reviews_by_film_id(self, id_film: int):
        """
        Récupère toutes les critiques d'un film donné par son identifiant.

        Parameters:
            id_film (int): L'ID du film.

        Returns:
            list: Liste des critiques pour ce film.
        """
        review = self.review_dao.get_all_review_by_id(id_film)
        if not review:
            raise ValueError("Pas de commentaires pour ce film")
        return review

    def get_reviews_by_user_id(self, id_user: int):
        """
        Récupère toutes les critiques d'un utilisateur
        donné par son identifiant.

        Parameters:
            id_user (int): L'ID de l'utilisateur.

        Returns:
            list: Liste des critiques pour cet utilisateur.
        """
        return self.review_dao.get_all_reviews_by_user_id(id_user)

    def get_review_by_user_and_film_id(self, id_user: int, id_film: int):
        """
        Récupère une critique spécifique d'un utilisateur
        donné pour un film donné.

        Parameters:
            id_user (int): L'ID de l'utilisateur.
            id_film (int): L'ID du film.

        Returns:
            Review: L'objet critique.
        """
        return self.review_dao.get_review_by_id_user_and_id_film(
            id_film, id_user
            )
