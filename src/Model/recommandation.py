import requests
from Movie import Movie


class recomandation:
    """
    Classe qui représente la méthode pour avoir une recommandation.

    Méthodes:
    ---------
    get_recommandation(id_film: int):
        Renvoie une liste de film en rapport avec le film appelé dans la méthode.
    """

    def get_recommandation(id_film: int):
        """
        Renvoie une liste de film en rapport avec le film appelé dans la méthode.

        Paramètres:
        -----------
        id_film : int
            Id du film qui va servir à avoir des recommandations.

        Returns:
        --------
            list[Movie]: liste de films recommandés par le film appelé par la méthode.
        """ ##à finir 



    API_KEY = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3YTM1YmQwMDE2Mzk5MDNmNWM4MzBlODhkZDg2ZWQzMCIsIm5iZiI6MTcyNjgxOTk4Mi42NzA1NDQsInN1YiI6IjY2ZTQ0NmI5OTAxM2ZlODcyMjI0MTc1MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.mUjUWmMcf2k7lyf4V7sJTn3X8eDGgYSpYDrhKippftg")  # Remplace par ta clé d'API TMDB

    def get_movie_id(title: str) -> int:
        """Récupère l'ID d'un film à partir de son titre."""
        search_url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}'
        response = requests.get(search_url)
        data = response.json()
    
        if data['results']:
            return data['results'][0]['id']
        else:
            raise ValueError("Film non trouvé.")

    def get_movie_details(movie_id: int):
        """Récupère les détails du film, y compris le réalisateur."""
        details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits'
        response = requests.get(details_url)
        data = response.json()
    
        # Récupérer l'ID du réalisateur
        director_id = None
        for crew in data['credits']['crew']:
            if crew['job'] == 'Director':
                director_id = crew['id']
                break
            
        return director_id

    def get_movies_by_director(director_id: int):
        """Récupère les films réalisés par le même réalisateur."""
        movies_url = f'https://api.themoviedb.org/3/person/{director_id}/movie_credits?api_key={API_KEY}'
        response = requests.get(movies_url)
        data = response.json()
    
        directed_movies = []
        for movie in data['crew']:
            directed_movies.append({
                'title': movie['title'],
                'release_date': movie['release_date'],
                'overview': movie['overview'],
                'vote_average': movie['vote_average'],
            })
    
        return directed_movies

    def recommend_movies(title: str):
        """Recommande des films similaires en fonction du titre donné et du réalisateur."""
        try:
            movie_id = get_movie_id(title)
            director_id = get_movie_details(movie_id)
            directed_movies = get_movies_by_director(director_id)
        
            if directed_movies:
                print(f"Films réalisés par le même réalisateur que '{title}':\n")
                for movie in directed_movies:
                    print(f"Title: {movie['title']}")
                    print(f"Release Date: {movie['release_date']}")
                    print(f"Overview: {movie['overview']}")
                    print(f"Average Rating: {movie['vote_average']}\n")
            else:
                print(f"Aucun film trouvé pour le réalisateur de '{title}'.")
        except ValueError as e:
            print(e)