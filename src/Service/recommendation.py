import requests
from sklearn.metrics.pairwise import cosine_similarity


class RecommendationService:
    """
    Service de recommandation de films basé sur la similarité des genres.
    """

    def __init__(self, api_key, access_token):
        """
        Initialise le service avec la clé API et le token d'accès.

        Parameters:
            api_key (str): La clé API pour accéder à TMDB.
            access_token (str): Le token d'accès pour authentifier
            les requêtes.
        """
        self.api_key = api_key
        self.access_token = access_token
        self.all_genres = self.get_tmdb_genres()
        self.movies = self.get_tmdb_movies(1000)
        self.similarity_matrix = self.calculate_similarity()

    def get_tmdb_genres(self):
        """
        Récupère la liste des genres de films depuis TMDB.

        Returns:
            list: Une liste des identifiants des genres disponibles.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={self.api_key}&language=en-US"
        response = requests.get(url, headers=headers)
        genres = response.json().get("genres", [])
        genre_ids = [genre["id"] for genre in genres]
        return genre_ids

    def get_tmdb_movies(self, num_movies=1000):
        """
        Récupère les films populaires depuis TMDB.

        Parameters:
            num_movies (int): Le nombre de films à récupérer (par défaut 1000).

        Returns:
            list: Une liste de films avec leurs informations.
        """

        movies = []
        page = 1
        headers = {"Authorization": f"Bearer {self.access_token}"}

        while len(movies) < num_movies:
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={self.api_key}&language=en-US&page={page}"
            response = requests.get(url, headers=headers)
            data = response.json()

            if "results" not in data:
                raise ValueError(
                    f"Erreur lors de la récupération des films : {data}"
                    )

            movies.extend(data["results"])
            page += 1
            if len(data["results"]) == 0:
                break

        return movies[:num_movies]

    def calculate_similarity(self):
        """
        Calcule la matrice de similarité des films basée sur les genres.

        Returns:
            array: Une matrice de similarité entre les films.
        """
        genre_matrix = []
        for movie in self.movies:
            genres = movie["genre_ids"]
            genre_vector = [
                1 if genre in genres else 0 for genre in self.all_genres
                ]
            genre_matrix.append(genre_vector)
        return cosine_similarity(genre_matrix)

    def recommend_movies(self, movie_id, top_n=5):
        """
        Recommande des films similaires à un film donné basé sur les genres.

        Parameters:
            movie_id (int): L'ID du film pour lequel
            on veut des recommandations.
            top_n (int): Le nombre de films
            recommandés à renvoyer (par défaut 5).

        Returns:
            list: Une liste des films recommandés.
        """
        try:
            idx = next(
                i for i,
                movie in enumerate(self.movies) if movie["id"] == movie_id
            )
        except StopIteration:
            return []

        similarities = self.similarity_matrix[idx]
        similar_indices = similarities.argsort()[-top_n - 1: -1][::-1]
        recommended_movies = [self.movies[i] for i in similar_indices]
        return recommended_movies
