class Film:
    def __init__(self, id_film: int, id_tmdb: int, title: str, producer: str, category: str, date: str):
        self.id_film = id_film
        self.id_tmdb = id_tmdb
        self.title = title
        self.producer = producer
        self.category = category
        self.date = date
        self.average_rate = 0.0
        self.ratings: List[int] = []

    def calculation_mean(self) -> float:
        """Calcule la note moyenne à partir des notes données."""
        if not self.ratings:
            return 0.0
        self.average_rate = sum(self.ratings) / len(self.ratings)
        return self.average_rate

    def add_rating(self, rating: int) -> None:
        """Ajoute une note à la liste et met à jour la note moyenne."""
        if 1 <= rating <= 10:
            self.ratings.append(rating)
            self.calculation_mean()
        else:
            raise ValueError("la note doit etre comprise entre 1 et 10")
        












