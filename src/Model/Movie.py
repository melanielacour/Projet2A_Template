# ################### Classe Movie ################################

class ValidationError(Exception):
    """Cette classe lève une exception pour les erreurs de validation."""
    pass


class Movie:
    """
    Cette classe représente un film avec ses attributs (identifiant,
    titre, réalisateur, genre, date, etc.). Elle est utilisée pour gérer
    les films dans l’application, qu’il s’agisse de films recherchés, notés
    ou commentés par les utilisateurs.

    Attributs:
    ----------
    id_film : int
        L'identifiant unique du film dans la base de données.
    id_tmdb: int
        L'identifiant du film sur TMDB.
    title : str
        Titre du film.
    producer : str
        Le nom du producteur ou réalisateur du film.
    category : str
        Genre du film.
    date : str
        Date de sortie du film.

    Méthodes:
    ---------
    calculation_mean(self): float
        Calcule la note moyenne.

    add_rating(self, rating: int) -> None:
        Ajoute une note à la liste de données.
    """

    def __init__(self, id_film, id_tmdb: int, title: str, producer: str, category: str, date: str):
        # Vérifie que id_film est un entier, sinon lève une ValidationError
        if not isinstance(id_film, int):
            try:
                # Convertit id_film en entier
                self.id_film = int(id_film)
                # Ou lève une exeption si c'est impossible
            except ValueError:
                raise ValueError("id_film must be an integer, unable to parse string as an integer")
        else:
            self.id_film = id_film  # Si c'est déjà un entier, il l'assigne directement

        # Vérifie que id_tmdb est un entier
        if not isinstance(id_tmdb, int):
            raise ValueError("id_tmdb must be an integer")

        self.id_tmdb = id_tmdb
        self.title = title
        self.producer = producer
        self.category = category
        self.date = date
        self.average_rate = 0.0
        self.ratings: list[int] = []

    def calculation_mean(self) -> float:
        """Méthode qui calcule la note moyenne à partir des notes données au film."""
        # Vérifie que des notes existent pour ce film
        if not self.ratings:
            return None
        # Formule de calcul de moyenne
        self.average_rate = sum(self.ratings) / len(self.ratings)
        return self.average_rate

    def add_rating(self, rating: int) -> None:
        """Méthode qui ajoute une note à la liste et met à jour la note moyenne.

        Paramètres:
        -----------
        rating : int
            La note à ajouter (elle doit être comprise entre 1 et 10)."""

        # Vérifie que la note est comprise entre 1 et 10
        if 1 <= rating <= 10:
            self.ratings.append(rating)
            self.calculation_mean()
        else:
            raise ValueError("la note doit etre comprise entre 1 et 10")
