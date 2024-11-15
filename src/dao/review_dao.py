from src.dao.db_connection import DBConnection
from src.Model.Review import Review
from src.utils.singleton import Singleton


class ReviewDao:
    def __init__(self, db_connection: DBConnection):
        self.db_connection = db_connection

    def get_all_review_by_id(self, id_film):
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.review WHERE id_film = %(id_film)s;",
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
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT review.* FROM projet_2a.film
                    JOIN projet_2a.review ON review.id_film = film.id
                    WHERE film.title = %(title)s;
                    """,
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

    def get_review_by_id_user_and_id_film(self, id_film, id_user):
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM projet_2a.review WHERE id_user = %(id_user)s AND id_film = %(id_film)s;",
                    {"id_user": id_user, "id_film": id_film}
                )
                res = cursor.fetchone()

        if res:
            return Review(
                id_review=res["id_review"],
                id_film=res["id_film"],
                id_user=res["id_user"],
                note=res["rating"],
                comment=res["comment"]
            )
        return None

    def add_review(self, review: Review):
        if not self.get_review_by_id_user_and_id_film(review.id_film, review.id_user):
            with self.db_connection.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO projet_2a.review (id_film, id_user, rating, comment)
                        VALUES (%(id_film)s, %(id_user)s, %(note)s, %(comment)s)
                        RETURNING id_review;
                        """,
                        {
                            "id_user": review.id_user,
                            "id_film": review.id_film,
                            "comment": review.comment,
                            "note": review.note
                        },
                    )
                    res1 = cursor.fetchone()

            if res1:
                return Review(
                    id_review=res1["id_review"],
                    id_user=review.id_user,
                    id_film=review.id_film,
                    comment=review.comment,
                    note=review.note
                )
            return False
        raise ValueError("Vous avez déjà commenté ce film.")

    def delete_review(self, id_user, id_film):
        rev = self.get_review_by_id_user_and_id_film(id_film, id_user)
        if rev:
            with self.db_connection.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM projet_2a.review WHERE id_user = %(id_user)s AND id_film = %(id_film)s;",
                        {"id_user": id_user, "id_film": id_film}
                    )
            return True
        return False

    def update_review(self, review: Review):
        """
        Met à jour une critique existante dans la base de données.
        """
        with self.db_connection.connection() as conn:
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

    def get_all_reviews_by_user_id(self, user_id):
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM projet_2a.review
                    WHERE review.id_user = %(user_id)s;
                    """,
                    {"user_id": user_id}
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
