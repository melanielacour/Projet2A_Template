from src.dao.db_connection import DBConnection
from src.Model.Review import Review


class ReviewDao:
    """
    Classe DAO pour gérer les opérations liées aux critiques de films.
    """

    def __init__(self, db_connection: DBConnection):
        """
        Initialise la classe avec une connexion à la base de données.

        Paramètres:
        -----------
        db_connection : DBConnection
            Objet de connexion à la base de données.
        """
        self.db_connection = db_connection

    def get_all_review_by_id(self, id_film):
        """
        Récupère toutes les critiques d'un film en fonction de son ID.

        Paramètres:
        -----------
        id_film : int
            Identifiant du film.

        Retourne:
        ---------
        list[Review]
            Liste des critiques pour le film spécifié.
        """
        query = "SELECT * FROM projet_2a.review WHERE id_film = %(id_film)s;"
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, {"id_film": id_film})
                res = cursor.fetchall()

        liste_review = []
        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                comment=row["comment"],
                note=row["rating"],
            )
            liste_review.append(review1)

        return liste_review

    def get_all_review_by_title(self, title):
        """
        Récupère toutes les critiques d'un film en fonction de son titre.

        Paramètres:
        -----------
        title : str
            Titre du film.

        Retourne:
        ---------
        list[Review]
            Liste des critiques pour le film spécifié.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT review.* FROM projet_2a.film
                    JOIN projet_2a.review ON review.id_film = film.id
                    WHERE film.title = %(title)s;
                    """,
                    {"title": title},
                )
                res = cursor.fetchall()

        liste_review = []
        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                comment=row["comment"],
                note=row["rating"],
            )
            liste_review.append(review1)

        return liste_review

    def get_review_by_id_user_and_id_film(self, id_film, id_user):
        """
        Récupère une critique par identifiant de film et d'utilisateur.

        Paramètres:
        -----------
        id_film : int
            Identifiant du film.
        id_user : int
            Identifiant de l'utilisateur.

        Retourne:
        ---------
        Review | None
            La critique correspondant aux identifiants ou None.
        """
        query = "SELECT * FROM projet_2a.review WHERE id_user = %(id_user)s"
        query += " AND id_film = %(id_film)s;"
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    query,
                    {"id_user": id_user, "id_film": id_film},
                )
                res = cursor.fetchone()

        if res:
            return Review(
                id_review=res["id_review"],
                id_film=res["id_film"],
                id_user=res["id_user"],
                note=res["rating"],
                comment=res["comment"],
            )
        return None

    def add_review(self, review: Review):
        """
        Ajoute une nouvelle critique pour un film par un utilisateur.

        Paramètres:
        -----------
        review : Review
            L'objet critique à ajouter.

        Retourne:
        ---------
        Review | False
            L'objet Review ajouté ou False si déjà existant.
        """
        rev = self.get_review_by_id_user_and_id_film(
            review.id_film, review.id_user
        )
        if not rev:
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
                            "note": review.note,
                        },
                    )
                    res1 = cursor.fetchone()

            if res1:
                return Review(
                    id_review=res1["id_review"],
                    id_user=review.id_user,
                    id_film=review.id_film,
                    comment=review.comment,
                    note=review.note,
                )
            return False
        raise ValueError("Vous avez déjà commenté ce film.")

    def delete_review(self, id_user, id_film):
        """
        Supprime une critique d'un film par un utilisateur.

        Paramètres:
        -----------
        id_user : int
            Identifiant de l'utilisateur.
        id_film : int
            Identifiant du film.

        Retourne:
        ---------
        bool
            True si la suppression est réussie, False sinon.
        """
        rev = self.get_review_by_id_user_and_id_film(id_film, id_user)
        if rev:
            query = "DELETE FROM projet_2a.review WHERE id_user = %(id_user)s"
            query += " AND id_film = %(id_film)s;"
            with self.db_connection.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, {
                        "id_user": id_user,
                        "id_film": id_film
                        })
            return True
        return False

    def update_review(self, review: Review):
        """
        Met à jour une critique existante dans la base de données.

        Paramètres:
        -----------
        review : Review
            L'objet critique à mettre à jour.

        Retourne:
        ---------
        Review
            L'objet critique mis à jour.
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
                        "id_review": review.id_review,
                    },
                )
        return review

    def get_all_reviews_by_user_id(self, user_id):
        """
        Récupère toutes les critiques d'un utilisateur en fonction de son ID.

        Paramètres:
        -----------
        user_id : int
            Identifiant de l'utilisateur.

        Retourne:
        ---------
        list[Review]
            Liste des critiques de l'utilisateur spécifié.
        """
        with self.db_connection.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT * FROM projet_2a.review
                    WHERE review.id_user = %(user_id)s;
                    """,
                    {"user_id": user_id},
                )
                res = cursor.fetchall()

        liste_review = []
        for row in res:
            review1 = Review(
                id_review=row["id_review"],
                id_film=row["id_film"],
                id_user=row["id_user"],
                comment=row["comment"],
                note=row["rating"],
            )
            liste_review.append(review1)

        return liste_review
