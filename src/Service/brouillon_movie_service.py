from typing import List, Optional

from src.Model.Movie import Movie


class MovieService:
    movie_db: Optional[object]

    def __init__(self, movie_db: Optional[object] = None):
        self.movie_db = movie_db

    def get_film_by_id(self, movie_id: int) -> Movie:
        # Récupération d'un film par ID
        return self.movie_db.get_film_by_id(movie_id)

    def get_all_film(self) -> List[Movie]:
        # Récupère tous les films depuis la base de données
        return self.movie_local.get_all_films()
