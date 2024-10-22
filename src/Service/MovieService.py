from typing import List, Optional

from src.Model.Movie import Movie


class MovieService:
    movie_db: Optional[object]
    tmdb_api_key: str = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTM1YmQwMDE2Mzk5MDNmNWM4MzBlODhkZDg2ZWQzMCIsIm5iZiI6MTcyNjgxOTk4Mi42NzA1NDQsInN1YiI6IjY2ZTQ0NmI5OTAxM2ZlODcyMjI0MTc1MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mUjUWmMcf2k7lyf4V7sJTn3X8eDGgYSpYDrhKippftg"

    def __init__(self, movie_db: Optional[object] = None):
        self.movie_db = movie_db

    def get_film_by_id(self, movie_id: int) -> Movie:
        # Récupération d'un film par ID depuis TMDB
        response = httpx.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.tmdb_api_key}&language=en-US")

        if response.status_code == 200:
            data = response.json()
            return Movie(id=data['id'], original_title=data['original_title'], description=data['overview'])
        else:
            raise Exception(f"Error retrieving movie: {response.status_code}")

    def get_all_films(self) -> List[Movie]:
        # Récupère tous les films depuis TMDB
        response = httpx.get(f"https://api.themoviedb.org/3/movie/popular?api_key={self.tmdb_api_key}&language=en-US&page=1")

        if response.status_code == 200:
            movies = response.json().get('results', [])
            return [Movie(id=movie['id'], original_title=movie['original_title'], description=movie['overview']) for movie in movies]
        else:
            raise Exception(f"Error retrieving movies: {response.status_code}")
