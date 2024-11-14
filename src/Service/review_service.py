import os

from dotenv import load_dotenv

from src.dao.db_connection import DBConnection
from src.dao.movie_local import MovieRepo
from src.dao.review_dao import ReviewDao
from src.Model.Review import Review

load_dotenv()

class ReviewService:
    def __init__(self, review_dao: ReviewDao):
        self.review_dao = review_dao

    def search_and_rate_movie_existing_movie(self, id_film, id_user, note, comment):
        # Vérifie si le film existe dans la base de données
        movie = MovieRepo(DBConnection()).get_movie_by_id_film(id_film)
        if not movie:
            raise ValueError("Identifiant de film incorrect")

        existing_review = self.review_dao.get_review_by_id_user_and_id_film(id_film, id_user)
        if existing_review:
            existing_review.note = note
            existing_review.comment = comment
            return self.update_review(existing_review)
        else:
            new_review = Review(id_review=None, id_film=id_film, id_user=id_user, note=note, comment=comment)
            return self.review_dao.add_review(new_review)

    def update_note(self, id_user,id_film,note):
        """
        Met à jour une critique existante dans la base de données.
        """
        existing_review=self.review_dao.get_review_by_id_user_and_id_film(id_film,id_user)
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        existing_review.note=note
        return self.review_dao.update_review(existing_review)

    def update_comment(self, id_user,id_film,comment):
        """
        Met à jour une critique existante dans la base de données.
        """
        existing_review=self.review_dao.get_review_by_id_user_and_id_film(id_film,id_user)
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        existing_review.comment=comment
        return self.review_dao.update_review(existing_review)

    def delete_review(self, id_film, id_user):
        """
        Supprime une critique spécifique pour un film par un utilisateur donné.
        """
        return self.review_dao.delete_review(id_user, id_film)

    def delete_note(self, id_film,id_user):
        existing_review=self.review_dao.get_review_by_id_user_and_id_film(id_film,id_user)
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        if not existing_review.comment:
            return self.delete_review(id_film=id_film, id_user=id_user)
        return self.update_note(id_film=id_film,id_user=id_user,note=None)
    def delete_comment(self, id_film,id_user):
        existing_review=self.review_dao.get_review_by_id_user_and_id_film(id_film,id_user)
        if not existing_review:
            raise ValueError("Vous n'avez ni commenté ni noté ce film")
        if not existing_review.note:
            return self.delete_review(id_film=id_film, id_user=id_user)
        return self.update_comment(id_film=id_film,id_user=id_user,comment=None)

    def get_average_rating(self, id_film):
        """
        Calcule la note moyenne des utilisateurs pour un film donné.
        """
        all_reviews = self.review_dao.get_all_review_by_id(id_film)
        if not all_reviews:
            return 0

        total_rating = sum(review.note for review in all_reviews)
        return total_rating / len(all_reviews)


    def search_and_rate_movie_by_idtmdb(self, id_tmdb, title, id_user, note, comment):
        movie = MovieRepo(DBConnection()).get_movie_by_tmdb_id(id_tmdb)
        if not movie:
            movie2 = MovieRepo(DBConnection()).add_movie(id_tmdb=id_tmdb, title=title)
            movie = MovieRepo(DBConnection()).get_movie_by_tmdb_id(id_tmdb)
            if not movie2:
                raise ValueError("Échec de l'ajout du film dans la base données")
        return self.search_and_rate_movie_existing_movie(movie.id_local, id_user, note, comment)
