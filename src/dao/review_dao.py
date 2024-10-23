from src.dao.db_connection import DBConnection
from src.Model.Movie import Movie
from src.Model.Review import Review
from src.utils.singleton import Singleton


class ReviewDao(metaclass=Singleton):
    def get_all_review_by_id(self, id_film):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_review,id_user,id_film,comment FROM projet_2a.review          "
                    "WHERE id = %(id_film)s;            ",
                    {"id_film": id_film}
                )
                res = cursor.fetchall()

        liste_review = []

        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                comment=row["comment"],
                note=row["rating"]
                )
            liste_review.append(review1)

        return liste_review

    def get_all_review_by_title(self, title):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.film                       "
                    "JOIN projet_2a.review ON review.id_film = film.id "
                    "WHERE film.title = %(title)s;                     ",
                    {"title": title}
                )
            res = cursor.fetchall()
        liste_review = []

        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                comment=row["comment"],
                note=row["rating"]
                )
            liste_review.append(review1)
            return liste_review

    def add_comment(self, review: Review):
        """
        Ajoute une critique au dictionnaire des critiques.

        Paramètres:
        -----------
        review_text : str
            Le texte de la critique à ajouter.
        """
        id_user = review.id_user
        id_film = review.id_film
        comment = review.comment
        note = review.note
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO projet_2a.review(id_film, id_user, rating, comment) "
                    "VALUES (%(id_user)s, %(id_film)s, %(note)s, %(comment)s) "
                    "RETURNING id_review; ",
                    {
                        "id_user": id_user,
                        "id_film": id_film,
                        "comment": comment,
                        "note": note
                    },
                )
                res1 = cursor.fetchone()

        if res1:
            rev = Review(
                id_review=res1["id_review"],
                id_user=id_user,
                id_film=id_film,
                comment=comment,
                note=note
            )
            return rev
        return False

    def delete_review(self, review):
        """
        Supprime la critique du dictionnaire des critiques.
        """
        if (self.id_user, self.id_film) in Review.reviews:
            del Review.reviews[(self.id_user, self.id_film)]
