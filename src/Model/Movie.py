# ################### Classe Movie ################################


class ValidationError(Exception):
    """Cette classe lève une exception pour les erreurs de validation."""

    pass


class Movie:
    """
    Cette classe représente un film avec ses attributs (identifiant,
    titre, réalisateur, genre, date, etc.).

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

    """

    def __init__(
        self, id_film, id_tmdb: int, title: str,
        producer: str, category: str, date: str
    ):
        # Vérifie que id_film est un entier, sinon lève une ValidationError
        if not isinstance(id_film, int):
            try:
                # Convertit id_film en entier
                self.id_film = int(id_film)
                # Ou lève une exeption si c'est impossible
            except ValueError:
                raise ValueError(
                    "id_film must be an integer, unable to parse string as"
                    + " an integer"
                )
        else:
            self.id_film = id_film

        if not isinstance(id_tmdb, int):
            raise ValueError("id_tmdb must be an integer")

        self.id_tmdb = id_tmdb
        self.title = title
        self.producer = producer
        self.category = category
        self.date = date
