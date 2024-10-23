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
                comment=row["comment"]
                )
            liste_review.append(review1)

        return liste_review

    def get_all_review_by_title(self, title):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.film                                  "
                    "JOIN projet_2a.review ON review.id_film = film.id            "
                    "WHERE film.title = %(title)s;                                 ",
                    {"title": title}
                )
            res = cursor.fetchall()
        liste_review = []

        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                comment=row["comment"]
                )
            liste_review.append(review1)
            return liste_review


    def add_review(self, review_text: str):
        """
        Ajoute une critique au dictionnaire des critiques.

        Paramètres:
        -----------
        review_text : str
            Le texte de la critique à ajouter.
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO projet_2a.users (pseudo, is_scout, password) "
                    "VALUES (%(pseudo)s, %(is_scout)s, %(pswd)s)              "
                    "RETURNING id;                                            ",
                    {
                        "pseudo": pseudo,
                        "is_scout": is_scout,
                        "pswd": pswd
                    },
                )
                res1 = cursor.fetchone()

        if res1:
            user1 = UserSimple(
                id_user=res1["id"],
                pseudo=pseudo,
                is_scout=is_scout,
                pswd=pswd
            )
            return True
        return False

    def delete_review(self):
        """
        Supprime la critique du dictionnaire des critiques.
        """
        if (self.id_user, self.id_film) in Review.reviews:
            del Review.reviews[(self.id_user, self.id_film)]
