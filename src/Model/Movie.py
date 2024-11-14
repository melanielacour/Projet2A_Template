class ValidationError(Exception):
    """Exception levée pour les erreurs de validation."""
    pass

class Movie:
    """
    Cette classe représente un film avec ses attributs (titre, réalisateur,
    catégorie, date, note moyenne, etc...). Elle est utilisée pour gérer les films dans
    l’application, qu’il s’agisse de films recherchés, notés ou commentés par les
    utilisateurs.

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
    
    def __init__(self, id_film, id_tmdb: int, title: str, producer: str, category: str, date: str):
        # Vérifie que id_film est un entier, sinon lève une ValidationError
        if not isinstance(id_film, int):
            try:
                # Essayez de convertir id_film en entier
                self.id_film = int(id_film)  # Convertit id_film en entier
            except ValueError:
                raise ValueError("id_film must be an integer, unable to parse string as an integer")
        else:
            self.id_film = id_film  # Si c'est déjà un entier, assigne-le directement

        # Vérifie que id_tmdb est un entier
        if not isinstance(id_tmdb, int):
            raise ValueError("id_tmdb must be an integer")

        self.id_tmdb = id_tmdb
        self.title = title
        self.producer = producer
        self.category = category
        self.date = date

