from src.dao.db_connection import DBConnection
from src.Model.Review import Review
from src.utils.singleton import Singleton

from src.Model.Movie import Movie


class ReviewDao(metaclass=Singleton):
    def get_all_review_by_id(self, id_film):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.review"
                    "WHERE id_film = %(id_film)s;            ",
                    {"id_film": id_film}
                )
                res = cursor.fetchall()

        liste_review = []

        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                review=row["review"]
                )
            liste_review.append(review1)

    def get_all_review_by_title(self, title):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.review                       "
                    "FROM projet_2a.film                                  "
                    "JOIN projet_2a.review ON review.id_film = film.id      "
                    "WHERE title = %(title)s;                             ",
                    {"title":title}
                )
        liste_review = []

        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                review=row["review"]
                )
            liste_review.append(review1)


    def add_review(self, review_text: str):
        """
        Ajoute une critique au dictionnaire des critiques.

        Paramètres:
        -----------
        review_text : str
            Le texte de la critique à ajouter.
        """
        Review.reviews[(self.id_user, self.id_film)] = review_text

    def delete_review(self):
        """
        Supprime la critique du dictionnaire des critiques.
        """
        if (self.id_user, self.id_film) in Review.reviews:
            del Review.reviews[(self.id_user, self.id_film)]
