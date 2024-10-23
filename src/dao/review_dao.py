from src.dao.db_connection import DBConnection
from src.Model.Movie import Movie
from src.Model.Review import Review
from src.utils.singleton import Singleton


class ReviewDao(metaclass=Singleton):
    def get_all_review_by_id(self, id_film):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                       "
                    "FROM projet_2a.review          "
                    "WHERE id_film = %(id_film)s;        ",
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

        return liste_review  # C'est ici que la liste devrait être retournée

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
    
    def get_review_by_id_user_and_id_film(self,id_film,id_user):
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                       "
                    "FROM projet_2a.review          "
                    "WHERE id_user = %(id_user)s    "
                    "   AND id_film =  %(id_film)s; ",
                    {
                        "id_user": id_user,
                        "id_film": id_film
                    },

                )
                res=cursor.fetchone()

        if res:
            rev=Review(
                id_review=res["id_review"],
                id_film=res["id_film"],
                id_user= res["id_user"],
                note=res["rating"],
                comment=res["comment"]

            )
            return rev

<<<<<<< HEAD
    def add_comment(self, review: Review):
=======


    def add_review(self,review: Review):
>>>>>>> 455843ac32d54422f97696732b59958562669d89
        """
        Ajoute une critique au dictionnaire des critiques.

        Paramètres:
        -----------
        review_text : str
            Le texte de la critique à ajouter.
        """
        id_user= review.id_user
        id_film= review.id_film
        comment= review.comment
        note= review.note
        if not self.get_review_by_id_user_and_id_film(id_user=id_user,id_film=id_film):

            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO projet_2a.review(id_film, id_user, rating, comment) "
                        "VALUES (%(id_film)s, %(id_user)s,%(note)s, %(comment)s)         "
                        "RETURNING id_review;                                            ",
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
        raise ValueError("Vous avez déja commenté ce film")

<<<<<<< HEAD
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
=======
    def delete_review(self, id_user, id_film):
>>>>>>> 455843ac32d54422f97696732b59958562669d89
        """
        Supprime la critique du dictionnaire des critiques.
        Retourne True si la suppression a été effectuée, False sinon.
        """
        rev = self.get_review_by_id_user_and_id_film(id_user, id_film)
        if rev:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet_2a.review  "
                        "WHERE id_user = %(id_user)s   "
                        "AND id_film = %(id_film)s;    ",
                        {
                            "id_user": id_user,
                            "id_film": id_film
                        },
                    )
            return True  # Suppression réussie
        return False  # La critique n'a pas été trouvée

