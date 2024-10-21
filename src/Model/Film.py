from typing import List


class Film:
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
    
    Méthodes:
    ---------
    calculation_mean(self) -> float:
        Calcule la note moyenne.

    add_rating(self, rating: int) -> None:
        Ajoute une note à la liste de données.
    """

    def __init__(self, id_film: int, id_tmdb: int, title: str, producer: str, category: str, date: str):
        self.id_film = id_film
        self.id_tmdb = id_tmdb
        self.title = title
        self.producer = producer
        self.category = category
        self.date = date
        self.average_rate = 0.0
        self.ratings: List[int] = []  # Liste pour stocker les notes

    def calculation_mean(self) -> float:
        """Calcule la note moyenne à partir des notes données au film.
        
        Retourne:
        ---------
        float: La note moyenne du film ou 0.0 si aucune note n'a été donnée.
        """
        if not self.ratings:
            return 0.0  # Retourne 0.0 si aucune note n'est disponible
        self.average_rate = sum(self.ratings) / len(self.ratings)
        return self.average_rate

    def add_rating(self, rating: int) -> None:
        """Ajoute une note à la liste et met à jour la note moyenne.
        
        Paramètres:
        -----------
        rating : int
            La note à ajouter (doit être comprise entre 1 et 10).
        """
        if 1 <= rating <= 10:
            self.ratings.append(rating)
            self.calculation_mean()  # Met à jour la note moyenne après ajout
        else:
            raise ValueError("La note doit être comprise entre 1 et 10.")
