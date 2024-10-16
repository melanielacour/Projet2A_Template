class Review:
    """
    Classe qui représente une critique d'un utilisateur sur un film.

    Attributs:
    ----------
    id_film : int
        L'identifiant du film critiqué.
    id_user : int
        L'identifiant de l'utilisateur qui a fait la critique.
    reviews : dict
        Un dictionnaire de critiques avec pour clé un tuple (id_user, id_film).

    Méthodes:
    ---------
    add_review():
        Ajoute une critique d'un film.

    delete_review():
        Supprime une critique d'un film.
    """

    reviews = {}

    def __init__(self, id_film: int, id_user: int):
        self.id_film = id_film
        self.id_user = id_user

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
