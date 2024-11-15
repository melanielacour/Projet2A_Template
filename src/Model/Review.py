class ValidationError(Exception):
    """Exception levée en cas d'erreur de validation des attributs."""
    pass


class Review:
    """
    Classe qui représente une critique d'un utilisateur sur un film.

    Attributs:
    ----------
    id_film : int
        L'identifiant du film critiqué.
    id_user : int
        L'identifiant de l'utilisateur qui a fait la critique.
    id_review : int
        L'identifiant du commentaire déposé.
    comment : str
        Le message du commentaire.
    note : int
        La note attribuée au film.
    """

    def __init__(self, id_film: int, id_user: int, id_review: int, comment: str, note: int):
        # Validation des types
        if not isinstance(id_film, int):
            raise ValidationError("id_film must be an integer")
        if not isinstance(id_user, int):
            raise ValidationError("id_user must be an integer")
        if not isinstance(comment, str):
            raise ValidationError("comment must be a string")
        if not isinstance(note, int) or not (0 <= note <= 10):
            raise ValidationError("note must be an integer between 0 and 10")

        self.id_film = id_film
        self.id_user = id_user
        self.id_review = id_review
        self.comment = comment
        self.note = note

    def __repr__(self):
        return (f"<Review(id_film={self.id_film}, id_user={self.id_user}, "
                f"id_review={self.id_review}, comment='{self.comment}', note={self.note})>")
