import os 
from src.dao.db_connection import DBConnection
from src.dao.review_dao import ReviewDao
from src.Model.Review import Review

class ReviewService:
    def __init__(self, review_dao: ReviewDao):
        self.review_dao = review_dao

    def search_and_rate_movie(self, id_film, id_user, note, comment):
        """
        Attribue une note à un film. Si une critique existe déjà, elle sera modifiée.
        """
        existing_review = self.review_dao.get_review_by_id_user_and_id_film(id_film, id_user)

        if existing_review:
            # Mise à jour de la critique existante
            existing_review.note = note
            existing_review.comment = comment
            return self.update_review(existing_review)
        else:
            # Ajout d'une nouvelle critique
            new_review = Review(
                id_review=None,  # L'ID sera généré automatiquement lors de l'ajout
                id_film=id_film,
                id_user=id_user,
                note=note,
                comment=comment
            )
            return self.review_dao.add_review(new_review)

    def update_review(self, review: Review):
        """
        Met à jour une critique existante dans la base de données.
        """
        with self.review_dao.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE projet_2a.review
                    SET rating = %(note)s, comment = %(comment)s
                    WHERE id_review = %(id_review)s;
                    """,
                    {
                        "note": review.note,
                        "comment": review.comment,
                        "id_review": review.id_review
                    }
                )
        return review

    def delete_review(self, id_film, id_user):
        """
        Supprime une critique spécifique pour un film par un utilisateur donné.
        """
        return self.review_dao.delete_review(id_user, id_film)

    def get_average_rating(self, id_film):
        """
        Calcule la note moyenne des utilisateurs pour un film donné.
        """
        all_reviews = self.review_dao.get_all_review_by_id(id_film)
        if not all_reviews:
            return 0

        total_rating = sum(review.note for review in all_reviews)
        return total_rating / len(all_reviews)
