class Rating:
    """
    Classe qui représente la note d'un utilisateur sur un film.

    Attributs:
    ----------
    id_film : int
        L'identifiant du film critiqué.
    id_user : int
        L'identifiant de l'utilisateur qui a fait la critique.
    id_review : int
        L'identifiant du commentaire déposé
    rate : str
        Le message du commentaire

    """

    def __init__(self, id_film: int, id_user: int, id_review: int, comment: str):
        self.id_film = id_film
        self.id_user = id_user
        self.id_review = id_review
        self.rate = rate
